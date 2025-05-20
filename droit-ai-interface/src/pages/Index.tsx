import React, { useState, useEffect, useRef } from 'react';
import { Send, Menu, FilePlus, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu';
import { ChatMessage } from '@/components/ChatMessage';
import { FileUpload } from '@/components/FileUpload';
import { ConversationHistory } from '@/components/ConversationHistory';
import { useUser } from '@/hooks/useUser';

const Index = () => {
  const { userId } = useUser();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [messages, setMessages] = useState<Array<{ text: string; isAi: boolean }>>([
    { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true },
  ]);
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<Array<{ title: string; date: string }>>([]);
  const [selectedTitle, setSelectedTitle] = useState<string | undefined>(
    localStorage.getItem('convTitle') || undefined
  );

  // **NOUVEAU** : état du mode d'envoi ('rag' ou 'llm')
  const [mode, setMode] = useState<'rag' | 'llm'>('rag');

  useEffect(() => {
    if (!userId) return;

    const fetchConversations = async () => {
      try {
        const res = await fetch(`http://localhost:8000/conversations/${userId}`);
        if (!res.ok) throw new Error('Erreur de chargement des conversations');
        const data = await res.json();
        setConversations(data);
      } catch (error) {
        console.error("Erreur de chargement des conversations :", error);
        setConversations([]);
      }
    };

    fetchConversations();
  }, [userId]);

  const handleSelectConversation = (title: string) => {
    localStorage.setItem('convTitle', title);
    setSelectedTitle(title);
    fetchMessagesForConversation(title);
  };

  const fetchMessagesForConversation = async (title: string) => {
    if (!userId) return;
    try {
      const res = await fetch(
        `http://localhost:8000/messages/${userId}/${encodeURIComponent(title)}`
      );
      if (!res.ok) throw new Error('Erreur lors du chargement des messages');

      const allMessages = await res.json();
      const formattedMessages = allMessages.map((msg: { message: string }) => ({
        text: msg.message,
        isAi: false,
      }));
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Erreur lors du chargement des messages :', error);
      setMessages([]);
    }
  };

  const handleSend = async () => {
    if (!input.trim() && files.length === 0) return;

    // Affiche immédiatement le message utilisateur
    setMessages((prev) => [...prev, { text: input, isAi: false }]);
    setInput('');
    setIsLoading(true);

    try {
      // Sélection de l'endpoint selon le mode
      const endpoint = mode === 'rag' ? 'send-message' : 'send-message-llm';
      const response = await fetch(`http://localhost:8000/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: parseInt(userId, 10),
          title: selectedTitle,
          message: input,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Affiche la réponse IA
        setMessages((prev) => [...prev, { text: data.answer, isAi: true }]);
      } else {
        console.error('Erreur send-message :', response.status, data);
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi au backend :", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (newFiles: File[]) => {
    setFiles((prev) => [...prev, ...newFiles]);
  };

  const handleRemoveFile = (name: string) => {
    setFiles((prev) => prev.filter((file) => file.name !== name));
  };

  const handleDeleteConversation = async (title: string) => {
    if (!confirm(`Supprimer la conversation "${title}" ?`)) return;
    try {
      const res = await fetch(
        `http://localhost:8000/conversations/${encodeURIComponent(title)}`,
        { method: 'DELETE' }
      );
      if (!res.ok) throw new Error("Erreur lors de la suppression");

      setConversations((prev) => prev.filter((conv) => conv.title !== title));

      if (selectedTitle === title) {
        localStorage.removeItem('convTitle');
        setSelectedTitle(undefined);
        setMessages([
          { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true },
        ]);
      }
    } catch (error) {
      console.error("Erreur lors de la suppression :", error);
    }
  };

  const startNewConversation = async () => {
    if (!userId) return;
    const title = prompt("Entrez le titre de la conversation :") || "Nouvelle conversation";
    const message = "Bonjour, comment puis-je vous aider ?";

    try {
      const res = await fetch('http://localhost:8000/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, title, message }),
      });

      if (res.ok) {
        const data = await res.json();
        console.log(data.message);

        setMessages([
          { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true },
        ]);
        setFiles([]);
        setSelectedTitle(title);
        localStorage.setItem('convTitle', title);

        const convRes = await fetch(`http://localhost:8000/conversations/${userId}`);
        const newData = await convRes.json();
        setConversations(newData);
      } else {
        console.error("Erreur lors de la création de la conversation");
      }
    } catch (error) {
      console.error("Erreur de communication avec le backend :", error);
    }
  };

  return (
    <div className="flex h-screen bg-background">
      <aside className="hidden md:flex w-80 border-r border-border flex-col p-4">
        <Button variant="outline" className="mb-4 w-full" onClick={startNewConversation}>
          Nouvelle conversation
        </Button>
        <ConversationHistory
          conversations={conversations}
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
                  conversations={conversations}
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
            {isLoading && <ChatMessage message="..." isAi={true} isLoading />}
          </div>
        </ScrollArea>

        <div className="p-4 border-t border-border glass">
          {files.length > 0 && (
            <div className="mb-4">
              <FileUpload onFileSelect={handleFileSelect} files={files} onRemoveFile={handleRemoveFile} />
            </div>
          )}
          <div className="flex gap-2 items-center">
            <Input
              placeholder="Posez votre question juridique..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1"
            />

            {/* DropdownMenu pour choisir le mode */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="shrink-0 flex items-center gap-1">
                  <Send className="h-4 w-4" />
                  {mode === 'rag' ? 'Envoyer (RAG)' : 'Envoyer (LLM)'}
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setMode('rag')}>
                  Envoyer avec RAG
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setMode('llm')}>
                  Envoyer avec LLM
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
              className="shrink-0"
            >
              <FilePlus className="h-4 w-4 mr-1" />
              Ajouter PDF
            </Button>
            <input
             type="file"
             ref={fileInputRef}
             accept="application/pdf"
             multiple
             style={{ display: 'none' }}
             onChange={(e) => {
               if (e.target.files) {
                 handleFileSelect(Array.from(e.target.files));
               }
             }}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
