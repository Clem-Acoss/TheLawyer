//ConversationHistory.tsx

import { MessageSquare } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

interface Conversation {
  id: string;
  title: string;
  date: string;
}

interface ConversationHistoryProps {
  conversations: Conversation[];
  onSelect: (id: string) => void;
  selectedId?: string;
}

export const ConversationHistory = ({ 
  conversations, 
  onSelect, 
  selectedId 
}: ConversationHistoryProps) => {
  return (
    <ScrollArea className="flex-1">
      <div className="space-y-2 p-2">
        {conversations.map((conv) => (
          <Button
            key={conv.id}
            variant={selectedId === conv.id ? "secondary" : "ghost"}
            className="w-full justify-start gap-2"
            onClick={() => onSelect(conv.id)}
          >
            <MessageSquare className="h-4 w-4" />
            <div className="flex-1 truncate text-left">
              <span className="text-sm">{conv.title}</span>
              <span className="block text-xs text-muted-foreground">{conv.date}</span>
            </div>
          </Button>
        ))}
      </div>
    </ScrollArea>
  );
};
