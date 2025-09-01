// components/chat/ChatInterface.tsx

import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { ChatMessage } from "@/components/ChatMessage";
import { FileUpload } from "../FileUpload";
import { FloatingButtons } from "@/components/ui/floatingButtons";

import { Loader2, Send } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";

interface ChatInterfaceProps {
  messages: any[]; // À typer mieux si tu as Message[]
  input: string;
  setInput: (val: string) => void;
  isSending: boolean;
  showUpload: boolean;
  onSend: () => void;
  onFileUpload: (file: File) => void;
  showFloatingButtons: boolean;
}

export const ChatInterface = ({
  messages,
  input,
  setInput,
  isSending,
  showUpload,
  onSend,
  onFileUpload,
  showFloatingButtons,
}: ChatInterfaceProps) => {
  return (
    <div className="flex-1 flex flex-col">
      <ScrollArea className="flex-1 px-4 py-4">
        <div className="flex flex-col gap-4 max-w-4xl mx-auto">
          {messages.map((message, idx) => (
            <ChatMessage key={idx} message={message} isAi={message.isAi} />
          ))}
        </div>
      </ScrollArea>

      <div className="p-4 border-t border-border glass flex flex-col gap-2 relative">
        <Textarea
          placeholder="Votre question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
        />
        <div className="flex justify-between">
          <FileUpload
            files={[]} // pas de fichiers pour l'instant
            onRemoveFile={(name: string) => {}} // fonction vide temporaire
            onFileSelect={(files: File[]) => {
            console.log("Fichiers sélectionnés :", files);
            }}
          />

          <Button onClick={onSend} disabled={isSending}>
            {isSending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Envoi...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Envoyer
              </>
            )}
          </Button>
        </div>

        {showFloatingButtons && <FloatingButtons />}
      </div>
    </div>
  );
};
