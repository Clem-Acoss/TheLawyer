/**
 * UserContext.tsx
 * 
 * Fournit un contexte React global pour la gestion de l'utilisateur connecté.
 * - Stocke le `userId` extrait du token JWT dans le state React.
 * - Fournit des fonctions de `login` (stocke le token + ID utilisateur) et `logout` (nettoyage).
 * - Permet un accès au contexte via le hook `useUser`.
 * 
 * Détails :
 * - Le token est stocké dans le `localStorage` pour persistance entre sessions.
 * - Le `userId` est décodé depuis la charge utile (payload) du JWT.
 * - Le hook `useUser` jette une erreur si utilisé hors du `UserProvider`.
 * 
 * Types :
 * - `UserContextType` définit les types des données et méthodes exposées dans le contexte.
 * 
 * Auteur : Clément Gardair  
 * Projet : PROJET-DROIT-IA-V2
 */

import React, { createContext, useContext, useState, ReactNode } from "react";

type UserContextType = {
  userId: string | null;
  login: (id: string, token: string) => void;
  logout: () => void;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

// Décodage simple du JWT pour extraire le sub = userId
function decodeUserId(token: string): string | null {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub;
  } catch {
    return null;
  }
}

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const initialToken = localStorage.getItem("token");
  const initialUserId = initialToken ? decodeUserId(initialToken) : null;
  const [userId, setUserId] = useState<string | null>(initialUserId);

  const login = (id: string, token: string) => {
    localStorage.setItem("token", token);
    setUserId(id);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUserId(null);
  };

  return (
    <UserContext.Provider value={{ userId, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within UserProvider");
  return context;
};
