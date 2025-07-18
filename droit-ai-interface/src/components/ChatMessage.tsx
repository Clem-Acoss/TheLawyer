/**
 * ChatMessage.tsx
 * 
 * Composant React permettant d’afficher un message dans l’interface de chat.
 * - Affiche un style spécifique si le message provient de l’IA ou de l’utilisateur.
 * - Affiche une animation de chargement pendant que la réponse est générée.
 * 
 * Props :
 * - message (ReactNode) : contenu du message à afficher.
 * - isAi (boolean) : indique si le message provient de l'IA (true) ou de l'utilisateur (false).
 * - isLoading (boolean, optionnel) : affiche un effet de chargement si la réponse est en attente.
 * 
 * Utilise les icônes `Bot` et `MessageSquare` depuis `lucide-react`.
 * Utilise la fonction utilitaire `cn` (lib/utils.ts) pour composer dynamiquement les classes Tailwind.
 * 
 * Auteur : Clement Gardair 
 * Projet : PROJET-DROIT-IA-V2
 */

import React, { ReactNode } from "react";
import { MessageSquare, Bot, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import ReactMarkdown from "react-markdown";

interface ChatMessageProps {
  message: string | ReactNode;
  isAi: boolean;
  isLoading?: boolean;
}

export const ChatMessage = ({ message, isAi, isLoading }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex items-start gap-3 p-4 rounded-lg",
        isAi ? "glass mr-12" : "ml-12 bg-primary/20"
      )}
    >
      <div
        className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center",
          isAi ? "bg-primary/20" : "bg-primary"
        )}
      >
        {isAi ? <Bot size={20} /> : <MessageSquare size={20} />}
      </div>
      <div className="flex-1 flex justify-between items-start">
        <div className="text-sm leading-relaxed">
          {isLoading ? (
            <div className="h-4 w-12 animate-pulse bg-muted rounded" />
          ) : (
            <ReactMarkdown>{String(message)}</ReactMarkdown>
          )}
        </div>
        {isAi && !isLoading && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="ml-2">
                <ChevronDown className="h-4 w-4" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => alert("Option 1 selected")}>
                Option 1
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => alert("Option 2 selected")}>
                Option 2
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => alert("Option 3 selected")}>
                Option 3
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )}
      </div>
    </div>
  );
};