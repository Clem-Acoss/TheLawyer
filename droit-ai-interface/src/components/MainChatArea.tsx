import React, { RefObject } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChatMessage } from "@/components/ChatMessage";
import { Skeleton } from "@/components/ui/skeleton";

type Message = {
  text: string;
  isAi: boolean;
};

type MainChatAreaProps = {
  messages: Message[];
  isLoading: boolean;
  messagesEndRef: RefObject<HTMLDivElement>;
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
          <ChatMessage key={i} message={msg.text} isAi={msg.isAi} />
        ))}
        {isLoading && (
          <ChatMessage
            message={
              <Skeleton className="h-6 w-20 rounded-md bg-muted animate-pulse" />
            }
            isAi={true}
          />
        )}
        <div ref={messagesEndRef} />
      </div>
    </ScrollArea>
  );
};
