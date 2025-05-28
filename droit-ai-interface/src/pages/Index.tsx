import React, { useState, useEffect, useRef } from "react";
import { Send, Menu, ChevronDown } from "lucide-react";
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
import { Skeleton } from "@/components/ui/skeleton";

type Conversation = {
  id: number;
  title: string;
  created_at: string;
};

type Message = {
  id: number;
  sender: string;
  content: string;
  created_at: string; // correction: timestamp renommé en created_at pour cohérence avec backend
};

const Index = () => {
  const { logout } = useUser();
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const [messages, setMessages] = useState<
    Array<{ text: string; isAi: boolean }>
  >([
    {
      text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?",
      isAi: true,
    },
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

  // Scroll automatique vers le bas quand messages ou isLoading changent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Chargement initial des conversations
  useEffect(() => {
    apiFetch<Conversation[]>(`/chat/conversations`)
      .then((data) => setConversations(data))
      .catch((e) => {
        console.error(e);
        setConversations([]);
      });
  }, []);

  const convForHistory = conversations.map((c) => ({
    title: c.title,
    date: new Date(c.created_at).toLocaleDateString("fr-FR"),
  }));

  const handleSelectConversation = (title: string) => {
    const conv = conversations.find((c) => c.title === title);
    if (conv) {
      setSelectedConvId(conv.id);
      setSelectedTitle(conv.title);
      localStorage.setItem("convTitle", conv.title);
      fetchMessages(conv.id);
    }
  };

  const fetchMessages = (convId: number) => {
    apiFetch<Message[]>(`/chat/messages/${convId}`)
      .then((all) =>
        setMessages(
          all.map((m) => ({
            text: m.content,
            isAi: m.sender !== "user",
          }))
        )
      )
      .catch((e) => {
        console.error(e);
        setMessages([]);
      });
  };

  const handleSend = async () => {
    if (!input.trim() && files.length === 0) return;
    if (selectedConvId === null) {
      alert("Veuillez sélectionner une conversation ou en créer une nouvelle.");
      return;
    }

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    // Ajout immédiat du message utilisateur dans l'UI
    setMessages((prev) => [...prev, { text: userMessage, isAi: false }]);

    try {
      if (mode === "rag") {
        const response = await apiFetch<{
          id: number;
          sender: string;
          content: string;
          created_at: string;
          is_ai: boolean;
        }>("/rag/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question: userMessage,
            conversation_id: selectedConvId,
          }),
    });
    console.log("Réponse API RAG :", response);
    setMessages((prev) => [
      ...prev,
      { text: response.content, isAi: true },
    ]);
      } else {
        // Envoi au backend LLM classique
        await apiFetch(`/chat/send-message-llm`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            conversation_id: selectedConvId,
            sender: "user",
            content: userMessage,
            is_ai: false,
          }),
        });

        // Recharge tous les messages
        const all = await apiFetch<Message[]>(`/chat/messages/${selectedConvId}`);
        setMessages(all.map((m) => ({ text: m.content, isAi: m.sender !== "user" })));
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const startNewConversation = async () => {
    const title = prompt("Entrez le titre de la conversation :") || "Nouvelle conversation";
    try {
      const conv = await apiFetch<Conversation>("/chat/conversation", {
        method: "POST",
        body: JSON.stringify({ title }),
      });
      handleSelectConversation(conv.title);
      const allConvs = await apiFetch<Conversation[]>(`/chat/conversations`);
      setConversations(allConvs);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteConversation = async (title: string) => {
    const conv = conversations.find((c) => c.title === title);
    if (!conv) return;

    if (!confirm(`Supprimer la conversation "${title}" ?`)) return;

    try {
      await apiFetch(`/chat/conversations/${conv.id}`, { method: "DELETE" });
      setConversations((prev) => prev.filter((c) => c.id !== conv.id));

      if (selectedConvId === conv.id) {
        setSelectedConvId(null);
        setSelectedTitle(undefined);
        setMessages([
          {
            text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?",
            isAi: true,
          },
        ]);
        localStorage.removeItem("convTitle");
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex h-screen bg-background">
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
            {isLoading && (
              <ChatMessage
                message={<Skeleton className="h-6 w-20 rounded-md bg-muted animate-pulse" />}
                isAi={true}
              />
            )}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        <div className="p-4 border-t border-border glass flex items-center gap-2">
          <Input
            placeholder="Posez votre question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={isLoading}
          />
          {/* Dropdown pour mode RAG / LLM */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="icon">
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem
                onClick={() => setMode("rag")}
                className={mode === "rag" ? "font-bold" : ""}
              >
                RAG
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setMode("llm")}
                className={mode === "llm" ? "font-bold" : ""}
              >
                LLM simple
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Button onClick={handleSend} disabled={isLoading} size="icon">
            <Send />
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Index;
