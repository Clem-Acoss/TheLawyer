import { MessageSquare, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

interface ConversationHistoryProps {
  conversations: { title: string; date: string }[];
  onSelect: (title: string) => void;
  onDelete: (title: string) => void;
  selectedTitle?: string;
}

export const ConversationHistory = ({ conversations, onSelect, onDelete, selectedTitle }: ConversationHistoryProps) => {
  return (
    <ScrollArea className="flex-1">
      <div className="space-y-2 p-2">
        {conversations.map((conv) => (
          <div key={conv.title} className="flex items-center justify-between">
            <Button
              variant={selectedTitle === conv.title ? "secondary" : "ghost"}
              className="flex-1 justify-start gap-2"
              onClick={() => onSelect(conv.title)}
            >
              <MessageSquare className="h-4 w-4" />
              <div className="flex-1 truncate text-left">
                <span className="text-sm">{conv.title}</span>
                <span className="block text-xs text-muted-foreground">{conv.date}</span>
              </div>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="ml-2"
              onClick={() => onDelete(conv.title)}
            >
              <Trash2 className="h-4 w-4 text-red-500 hover:text-red-700" />
            </Button>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
};
