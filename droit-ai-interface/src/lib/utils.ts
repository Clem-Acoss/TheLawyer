/**
 * utils.ts
 * 
 * Utilitaires pour la gestion des classes CSS avec Tailwind et clsx.
 * 
 * Fonction principale :
 * - `cn(...inputs: ClassValue[])` : combine et fusionne les classes CSS en gérant les conflits Tailwind.
 * 
 * Détails :
 * - Utilise `clsx` pour la concaténation conditionnelle des classes.
 * - Utilise `tailwind-merge` pour fusionner proprement les classes Tailwind en conflit.
 * 
 * Auteur : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */



import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
