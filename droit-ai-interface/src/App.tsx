// App.tsx
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
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </UserProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
