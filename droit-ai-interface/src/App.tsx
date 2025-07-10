/**
 * App.tsx
 * 
 * Composant racine principal de l’application React.
 * 
 * Fonctionnalités principales :
 * - Configuration du provider React Query pour la gestion des requêtes asynchrones.
 * - Fourniture du contexte utilisateur global via UserProvider.
 * - Intégration de composants UI globaux : Toaster pour notifications, TooltipProvider pour infobulles.
 * - Configuration du routage avec react-router-dom :
 *    - Route "/" vers la page d'inscription.
 *    - Route "/login" vers la page de connexion.
 *    - Route "/Index" vers la page principale après authentification.
 *    - Route "*" pour la gestion des pages non trouvées (404).
 * 
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */

import { UserProvider } from "@/context/UserContext";  // Import du contexte utilisateur
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Register from "./pages/register";
import Login from "./pages/login";
import ResetPassword from "./pages/reset_password";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <UserProvider> {/* Enveloppe toute l’app avec UserProvider */}
        <BrowserRouter>
          <Routes>
            <Route path="/Index" element={<Index />} />        {/* Page d'accueil après connexion */}
            <Route path="/" element={<Register />} />          {/* Page d'inscription */}
            <Route path="/login" element={<Login />} />        {/* Page de connexion */}
            <Route path="/password/reset" element={<ResetPassword />} /> {/* Page de reset mdp */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </UserProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
