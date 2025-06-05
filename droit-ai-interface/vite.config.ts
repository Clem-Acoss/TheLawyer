import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

/**
 * vite.config.ts
 *
 * Configuration de Vite pour le projet Droit AI Interface.
 *
 * Principales fonctionnalités :
 * - Configuration du serveur de développement avec un proxy pour les requêtes RAG.
 * - Intégration de plugins React et Lovable Tagger pour la gestion des composants.
 * - Résolution des chemins d'importation avec des alias.
 *
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 8080,
    proxy: {
      '/rag': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
