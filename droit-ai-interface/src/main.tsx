/**
 * main.tsx
 * 
 * Point d'entrée principal de l'application React.
 * 
 * Fonctionnalités principales :
 * - Monte le composant racine <App /> dans l'élément DOM avec l'id "root".
 * - Importe les styles globaux depuis index.css.
 * - Utilise la méthode createRoot de React 18 pour le rendu.
 * 
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */


import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById("root")!).render(<App />);
