/**
 * use-mobile.tsx
 * 
 * Hook personnalisé React pour détecter si l'utilisateur est sur un appareil mobile.
 * - Utilise `window.matchMedia` pour écouter les changements de taille d'écran.
 * - Retourne un booléen indiquant si la fenêtre est inférieure au breakpoint mobile.
 * 
 * Caractéristiques :
 * - Breakpoint mobile défini à 768px.
 * - Réagit dynamiquement aux redimensionnements de la fenêtre.
 * 
 * Usage typique :
 * ```tsx
 * const isMobile = useIsMobile();
 * ```
 * 
 * Auteur : Clément Gardair  
 * Projet : PROJET-DROIT-IA-V2
 */

import * as React from "react"

const MOBILE_BREAKPOINT = 768

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }
    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    return () => mql.removeEventListener("change", onChange)
  }, [])

  return !!isMobile
}
