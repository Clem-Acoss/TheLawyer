import React, { useState, useEffect, useRef } from "react";
import { Send, Menu, FilePlus, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import { ChatMessage } from "@/components/ChatMessage";
import { FileUpload } from "@/components/FileUpload";
import { ConversationHistory } from "@/components/ConversationHistory";
import { useUser } from "@/context/UserContext";
import { apiFetch } from "@/lib/api";

type Conversation = {
  id: number;
  title: string;
  created_at: string;
};

type Message = {
  id: number;
  sender: string;
  content: string;
  timestamp: string;
};

const Index = () => {
  const { userId, logout } = useUser();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [messages, setMessages] = useState<Array<{ text: string; isAi: boolean }>>([
    { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true },
  ]);
  const [input, setInput] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConvId, setSelectedConvId] = useState<number | null>(null);
  const [selectedTitle, setSelectedTitle] = useState<string | undefined>(
    localStorage.getItem("convTitle") || undefined
  );
  const [mode, setMode] = useState<"rag" | "llm">("rag");

  // Charger les conversations
  useEffect(() => {
    if (!userId) return;
    apiFetch<Conversation[]>(`/chat/conversations/${userId}`)
      .then((data) => setConversations(data))
      .catch((e) => {
        console.error(e);
        setConversations([]);
      });
  }, [userId]);

  // Construire la liste au format attendu par ConversationHistory
  const convForHistory = conversations.map((c) => ({
    title: c.title,
    date: new Date(c.created_at).toLocaleDateString("fr-FR"),
  }));

  // Sélectionner une conversation via le title
  const handleSelectConversation = (title: string) => {
    const conv = conversations.find((c) => c.title === title);
    if (conv) {
      setSelectedConvId(conv.id);
      setSelectedTitle(conv.title);
      localStorage.setItem("convTitle", conv.title);
      fetchMessages(conv.id);
    }
  };

  // Récupérer les messages
  const fetchMessages = (convId: number) => {
    apiFetch<Message[]>(`/chat/messages/${convId}`)
      .then((all) =>
        setMessages(
          all.map((m) => ({ text: m.content, isAi: m.sender !== userId }))
        )
      )
      .catch((e) => {
        console.error(e);
        setMessages([]);
      });
  };

  // Envoyer un message
  const handleSend = async () => {
    if (!input.trim() && files.length === 0) return;
    setMessages((prev) => [...prev, { text: input, isAi: false }]);
    setInput("");
    setIsLoading(true);

    try {
      const endpoint = mode === "rag" ? "send-message" : "send-message-llm";
      const data = await apiFetch<{ answer: string }>(
        `/chat/${endpoint}`,
        {
          method: "POST",
          body: JSON.stringify({
            conversation_id: selectedConvId,
            sender: userId,
            content: input,
          }),
        }
      );
      setMessages((prev) => [...prev, { text: data.answer, isAi: true }]);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  // Créer une nouvelle conversation
  const startNewConversation = async () => {
    if (!userId) return;
    const title = prompt("Entrez le titre de la conversation :") || "Nouvelle conversation";
    try {
      const conv = await apiFetch<Conversation>(
        "/chat/conversation",
        {
          method: "POST",
          body: JSON.stringify({ user_id: userId, title }),
        }
      );
      handleSelectConversation(conv.title);
      // Recharger la liste
      const allConvs = await apiFetch<Conversation[]>(`/chat/conversations/${userId}`);
      setConversations(allConvs);
    } catch (e) {
      console.error(e);
    }
  };

  // Supprimer une conversation via le title
  const handleDeleteConversation = async (title: string) => {
    const conv = conversations.find((c) => c.title === title);
    if (!conv) return;

    if (!confirm(`Supprimer la conversation "${title}" ?`)) return;

    try {
      await apiFetch(`/chat/conversations/${conv.id}`, {
        method: "DELETE",
        body: JSON.stringify({ user_id: userId }),
      });
      setConversations((prev) => prev.filter((c) => c.id !== conv.id));

      if (selectedConvId === conv.id) {
        setSelectedConvId(null);
        setSelectedTitle(undefined);
        setMessages([
          { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true },
        ]);
        localStorage.removeItem("convTitle");
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (!userId) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p>Utilisateur non authentifié. <Button onClick={() => logout()}>Se déconnecter</Button></p>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="hidden md:flex w-80 border-r border-border flex-col p-4">
        <Button variant="outline" className="mb-4 w-full" onClick={startNewConversation}>
          Nouvelle conversation
        </Button>
        <ConversationHistory
          conversations={convForHistory}
          onSelect={handleSelectConversation}
          onDelete={handleDeleteConversation}
          selectedTitle={selectedTitle}
        />
        {conversations.length === 0 && <p>Aucune conversation disponible</p>}
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        <header className="h-14 border-b border-border flex items-center px-4 glass">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-80 sm:w-96">
              <SheetHeader>
                <SheetTitle>Conversations</SheetTitle>
                <SheetDescription>Gérez vos conversations existantes</SheetDescription>
              </SheetHeader>
              <div className="flex flex-col h-full mt-4">
                <Button variant="outline" className="mb-4" onClick={startNewConversation}>
                  Nouvelle conversation
                </Button>
                <ConversationHistory
                  conversations={convForHistory}
                  onSelect={handleSelectConversation}
                  onDelete={handleDeleteConversation}
                  selectedTitle={selectedTitle}
                />
              </div>
            </SheetContent>
          </Sheet>
          <h1 className="text-lg font-semibold ml-4">Assistant Juridique</h1>
        </header>

        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((msg, i) => (
              <ChatMessage key={i} message={msg.text} isAi={msg.isAi} />
            ))}
            {isLoading && <ChatMessage message="..." isAi />}
          </div>
        </ScrollArea>

        <div className="p-4 border-t border-border glass">
          {files.length > 0 && (
            <div className="mb-4">
              <FileUpload onFileSelect={() => {}} files={files} onRemoveFile={() => {}} />
            </div>
          )}
          <div className="flex gap-2 items-center">
            <Input
              placeholder="Posez votre question juridique..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              className="flex-1"
            />

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="shrink-0 flex items-center gap-1">
                  <Send className="h-4 w-4" />
                  {mode === "rag" ? "Envoyer (RAG)" : "Envoyer (LLM)"}
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setMode("rag")}>
                  Envoyer avec RAG
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setMode("llm")}>
                  Envoyer avec LLM
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Button variant="outline" onClick={() => fileInputRef.current?.click()} className="shrink-0">
              <FilePlus className="h-5 w-5" />
            </Button>
            <input
              type="file"
              multiple
              ref={fileInputRef}
              className="hidden"
              onChange={(e) => {
                if (!e.target.files) return;
                setFiles(Array.from(e.target.files));
              }}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
