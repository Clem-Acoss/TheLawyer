/**
 * src/pages/Register.tsx
 * 
 * Composant React de la page d'inscription utilisateur.
 * 
 * Fonctionnalités principales :
 * - Formulaire d'inscription avec saisie email et mot de passe.
 * - Envoi des données JSON à l’API d’enregistrement utilisateur.
 * - Navigation vers la page de connexion après inscription réussie.
 * - Gestion des erreurs et affichage de messages d’alerte.
 * 
 * Hooks React utilisés :
 * - useState pour la gestion des champs de formulaire et du statut de chargement.
 * - useNavigate pour la navigation programmatique après inscription.
 * 
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "@/lib/api";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    setIsLoading(true);
    try {
      await apiFetch("/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      navigate("/login");
    } catch (error: any) {
      console.error("Erreur d'inscription :", error);
      alert(error.message || "Erreur lors de l'inscription.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="glass p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">
          Créer un compte
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
            onClick={handleRegister}
            disabled={isLoading}
          >
            {isLoading ? "Création..." : "S'inscrire"}
          </Button>
        </div>
        <p className="mt-4 text-center text-sm text-muted-foreground">
          Déjà un compte ?{" "}
          <Link to="/login" className="text-primary underline">
            Se connecter
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
