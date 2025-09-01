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
import React from "react";
import { MessageSquare, Bot, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import ReactMarkdown from "react-markdown";
import { Skeleton } from "@/components/ui/skeleton";

// Type pour un message IA avec chunks
interface AIMessage {
  content: string;
  chunks?: Array<{ node_text?: string }>;
}

// Type pour le contenu du message : string simple ou message IA
type ChatMessageContent = string | AIMessage;

interface ChatMessageProps {
  message: ChatMessageContent;
  isAi: boolean;
  isLoading?: boolean;
}

export const ChatMessage = ({ message, isAi, isLoading }: ChatMessageProps) => {
  const renderMessageContent = (): JSX.Element => {
    if (isLoading) {
      return <Skeleton className="h-6 w-full rounded-md bg-muted animate-pulse" />;
    }

    if (typeof message === "string") {
      return <ReactMarkdown>{message}</ReactMarkdown>;
    }

    return <ReactMarkdown>{message.content}</ReactMarkdown>;
  };

  const filteredChunks =
    typeof message !== "string" && message.chunks
      ? message.chunks.filter((chunk) => chunk.node_text?.trim())
      : [];

  return (
    <div
      className={cn(
        "flex items-start gap-3 p-4 rounded-lg",
        isAi ? "glass mr-12" : "ml-12 bg-primary/20"
      )}
    >
      {/* Icône */}
      <div
        className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center",
          isAi ? "bg-primary/20" : "bg-primary"
        )}
      >
        {isAi ? <Bot size={20} /> : <MessageSquare size={20} />}
      </div>

      {/* Contenu + chevron */}
      <div className="flex-1">
        <div className="flex justify-between items-start">
          <div className="text-sm leading-relaxed w-full">{renderMessageContent()}</div>

          {/* Chevron pour IA */}
          {isAi && !isLoading && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="ml-2 p-1 rounded-md bg-gray-200 hover:bg-gray-300">
                  <ChevronDown className="h-4 w-4 text-gray-700" />
                </button>
              </DropdownMenuTrigger>

              <DropdownMenuContent
                side="left"       // ouvre à gauche du trigger
                align="end"       // bord droit du dropdown aligné avec le trigger
                sideOffset={4}    // décale légèrement du trigger
                className="max-h-64 w-80 overflow-y-auto p-2" // scroll vertical si contenu long
              >
                {filteredChunks.length > 0 ? (
                  filteredChunks.map((chunk, index) => (
                    <DropdownMenuItem key={index} title={chunk.node_text}>
                      {chunk.node_text || "Pas de contenu"}
                    </DropdownMenuItem>
                  ))
                ) : (
                  <DropdownMenuItem disabled>Aucun contexte disponible</DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </div>
  );
};
