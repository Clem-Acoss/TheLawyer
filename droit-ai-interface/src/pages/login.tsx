/**
 * login.tsx
 * 
 * Composant React de la page de connexion utilisateur.
 * 
 * Fonctionnalités principales :
 * - Formulaire de connexion avec saisie email et mot de passe.
 * - Envoi des données en application/x-www-form-urlencoded à l’API d’authentification.
 * - Décodage du token JWT reçu pour extraire l’identifiant utilisateur.
 * - Mise à jour du contexte utilisateur avec l’état de connexion.
 * - Redirection vers la page principale après connexion réussie.
 * - Gestion des erreurs et affichage de messages d’alerte.
 * 
 * Hooks React utilisés :
 * - useState pour la gestion des champs de formulaire et du statut de chargement.
 * - useNavigate pour la navigation programmatique après connexion.
 * 
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */


import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { useUser } from "@/context/UserContext";
import { apiFetch } from "@/lib/api";
import { ErrorModal } from "@/components/errorModal";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();
  const { login } = useUser();

  const handleLogin = async () => {
    setIsLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const data = await apiFetch<{ access_token: string; token_type: string }>(
        "/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData.toString(),
        }
      );

      const token = data.access_token;
      const payload = JSON.parse(atob(token.split(".")[1]));
      login(payload.sub, token);

      navigate("/Index");
    } catch (error: any) {
      console.error("Erreur de connexion :", error);
      setErrorMessage(error.message || "Erreur de connexion.");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordResetRequest = async () => {
    if (!email) {
      setErrorMessage("Veuillez d'abord renseigner votre email.");
      return;
    }
    setIsResetting(true);
    try {
      await apiFetch("/auth/password-reset/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      setErrorMessage("Un lien de réinitialisation a été envoyé à votre email.");
    } catch (error: any) {
      console.error("Erreur reset password:", error);
      setErrorMessage(error.message || "Erreur lors de la demande de réinitialisation.");
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <>
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="glass p-8 rounded-2xl shadow-lg w-full max-w-md">
          <h1 className="text-2xl font-semibold mb-6 text-center">
            Se connecter
          </h1>
          <div className="space-y-4">
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              type="password"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              className="w-full"
              onClick={handleLogin}
              disabled={isLoading}
            >
              {isLoading ? "Connexion..." : "Se connecter"}
            </Button>
          </div>
          <div className="mt-4 text-center text-sm text-muted-foreground space-y-2">
            <p>
              Pas encore de compte ?{" "}
              <Link to="/register" className="text-primary underline">
                S'inscrire
              </Link>
            </p>
            <p>
              <button
                className="text-primary underline"
                onClick={handlePasswordResetRequest}
                disabled={isResetting}
              >
                {isResetting ? "Envoi en cours..." : "Mot de passe oublié ?"}
              </button>
            </p>
          </div>
        </div>
      </div>

      <ErrorModal
        open={errorMessage !== null}
        description={errorMessage || ""}
        onClose={() => setErrorMessage(null)}
      />
    </>
  );
};

export default Login;