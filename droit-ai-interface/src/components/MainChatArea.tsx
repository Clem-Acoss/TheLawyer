import React, { RefObject } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChatMessage } from "@/components/ChatMessage";
import { Skeleton } from "@/components/ui/skeleton";


export type ChatMessage = {
  message: string | { content: string; chunks?: Array<{ node_text?: string }> };
  isAi: boolean;
};
type MainChatAreaProps = {
  messages: ChatMessage[];
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement>;
};

export const MainChatArea: React.FC<MainChatAreaProps> = ({
  messages,
  isLoading,
  messagesEndRef,
}) => {
  return (
    <ScrollArea className="flex-1 p-4">
      <div className="space-y-4">
        {messages.map((msg, i) => (
          <ChatMessage
            key={i}
            message={msg.message}  // on passe directement le message au composant
            isAi={msg.isAi}
          />
        ))}

        {/* Loader */}
        {isLoading && (
          <ChatMessage
            message="Chargement..."
            isAi={true}
          />
        )}

        <div ref={messagesEndRef} />
      </div>
    </ScrollArea>
  );
};