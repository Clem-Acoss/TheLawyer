// ChatMessage.tsx


import React from 'react';
import { MessageSquare, Bot } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: string;
  isAi: boolean;
  isLoading?: boolean;
}

export const ChatMessage = ({ message, isAi, isLoading }: ChatMessageProps) => {
  return (
    <div className={cn(
      "flex items-start gap-3 p-4 rounded-lg",
      isAi ? "glass mr-12" : "ml-12 bg-primary/20"
    )}>
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center",
        isAi ? "bg-primary/20" : "bg-primary"
      )}>
        {isAi ? <Bot size={20} /> : <MessageSquare size={20} />}
      </div>
      <div className="flex-1">
        {isLoading ? (
          <div className="h-4 w-12 animate-pulse bg-muted rounded" />
        ) : (
          <p className="text-sm leading-relaxed">{message}</p>
        )}
      </div>
    </div>
  );
};
