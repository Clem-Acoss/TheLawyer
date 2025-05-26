// src/context/UserContext.tsx
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
