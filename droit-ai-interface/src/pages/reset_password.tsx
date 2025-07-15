/**
 * reset_password.tsx
 *
 * Page de réinitialisation de mot de passe.
 * - Lit le token depuis l'URL (`?token=...`)
 * - Affiche un formulaire de nouveau mot de passe
 * - Envoie les données au backend pour mise à jour
 *
 * Auteur : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */

import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiFetch } from "@/lib/api";
import { ErrorModal } from "@/components/errorModal";

const ResetPassword= () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setErrorMessage("Lien invalide ou expiré.");
    }
  }, [token]);

  const handleReset = async () => {
    if (!token) return;

    if (newPassword !== confirmPassword) {
      setErrorMessage("Les mots de passe ne correspondent pas.");
      return;
    }

    setIsLoading(true);
    try {
      await apiFetch("/auth/password-reset/confirm", {
        method: "POST",
        body: JSON.stringify({
          token,
          new_password: newPassword,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      setSuccessMessage("Mot de passe mis à jour. Redirection...");
      setTimeout(() => navigate("/login"), 3000);
    } catch (error: any) {
      console.error("Erreur reset:", error);
      setErrorMessage(error.message || "Erreur de réinitialisation.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="glass p-8 rounded-2xl shadow-lg w-full max-w-md">
          <h1 className="text-2xl font-semibold mb-6 text-center">
            Réinitialiser le mot de passe
          </h1>

          {successMessage ? (
            <p className="text-green-400 text-center">{successMessage}</p>
          ) : (
            <div className="space-y-4">
              <Input
                type="password"
                placeholder="Nouveau mot de passe"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Confirmer le mot de passe"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <Button
                className="w-full"
                onClick={handleReset}
                disabled={isLoading || !token}
              >
                {isLoading ? "Mise à jour..." : "Réinitialiser"}
              </Button>
            </div>
          )}
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

export default ResetPassword;