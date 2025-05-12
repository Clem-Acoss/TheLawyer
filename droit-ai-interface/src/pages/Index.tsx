// index.tsx 



import React, { useState, useEffect } from 'react';
import { Send, Menu } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { ChatMessage } from '@/components/ChatMessage';
import { FileUpload } from '@/components/FileUpload';
import { ConversationHistory } from '@/components/ConversationHistory';
import { useUser } from '@/hooks/useUser'; // <-- import du hook
import {SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';

const Index = () => {
  const { userId } = useUser(); // <-- récup du user connecté
  const [messages, setMessages] = useState<Array<{ text: string; isAi: boolean }>>([
    { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true }
  ]);
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<Array<{ id: string, title: string, date: string }>>([]);

  // Récupérer les conversations depuis le backend
  useEffect(() => {
    if (!userId) return; // Si l'utilisateur n'est pas connecté, on ne fait rien
    const fetchConversations = async () => {
      try {
        const res = await fetch(`http://localhost:8000/conversations/${userId}`);
        if (!res.ok) {
          throw new Error('Erreur de chargement des conversations');
        }
        const data = await res.json();
        console.log(data);
        setConversations(data);
      } catch (error) {
        console.error("Erreur de chargement des conversations :", error);
        setConversations([]); // Assure-toi que les conversations soient vides en cas d'erreur
      }
    };
  
    fetchConversations();
  }, [userId]);
  

  const handleSend = async () => {
    if (!input.trim() && files.length === 0) return;

    const newMessage = { text: input, isAi: false };
    setMessages(prev => [...prev, newMessage]);
    setInput('');
    setIsLoading(true);

    const formData = new FormData();
    formData.append('message', input);
    if (userId) formData.append('user_id', userId); // <-- envoi userId dans le formData
    files.forEach(file => formData.append('files', file));

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      setMessages(prev => [...prev, {
        text: data.response,
        isAi: true
      }]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi au backend :', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (newFiles: File[]) => {
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleRemoveFile = (name: string) => {
    setFiles(prev => prev.filter(file => file.name !== name));
  };

  const startNewConversation = async () => {
    if (!userId) return;
  
    // Afficher un prompt pour saisir le titre de la conversation
    const title = prompt("Entrez le titre de la conversation :") || "Nouvelle conversation"; // Titre par défaut si non saisi
    const message = "Bonjour, comment puis-je vous aider ?"; // Message initial
  
    // Envoi de la requête POST pour créer la conversation
    try {
      const response = await fetch('http://localhost:8000/conversations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          title: title,
          message: message,
        }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log(data.message); // Afficher la réponse du backend (si succès)
  
        // Mettre à jour l'état pour démarrer une nouvelle conversation dans le frontend
        setMessages([
          { text: "Bonjour, je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?", isAi: true }
        ]);
        setFiles([]); // Réinitialiser les fichiers
  
        // Recharger les conversations
        const fetchConversations = async () => {
          const res = await fetch(`http://localhost:8000/conversations/${userId}`);
          const data = await res.json();
          setConversations(data);  // Mettre à jour l'état des conversations
        };
  
        fetchConversations();
      } else {
        console.error("Erreur lors de la création de la conversation");
      }
    } catch (error) {
      console.error("Erreur de communication avec le backend :", error);
    }
  };
  

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="hidden md:flex w-80 border-r border-border flex-col p-4">
        <Button 
          variant="outline" 
          className="mb-4 w-full"
          onClick={startNewConversation}
        >
          Nouvelle conversation
        </Button>
        <ConversationHistory 
          conversations={conversations}
          onSelect={() => {}}
        />
        {conversations.length === 0 && <p>Aucune conversation disponible</p>}
      </aside>

      {/* Main chat area */}
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
              <Button 
                variant="outline" 
                className="mb-4"
                onClick={startNewConversation}
              >
                Nouvelle conversation
              </Button>
              <ConversationHistory 
                conversations={conversations}
                onSelect={() => {}}
              />
            </div>
          </SheetContent>
        </Sheet>
          <h1 className="text-lg font-semibold ml-4">Assistant Juridique</h1>
        </header>

        {/* Messages area */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((msg, i) => (
              <ChatMessage 
                key={i}
                message={msg.text}
                isAi={msg.isAi}
              />
            ))}
            {isLoading && (
              <ChatMessage 
                message="..."
                isAi={true}
                isLoading={true}
              />
            )}
          </div>
        </ScrollArea>

        {/* Input area */}
        <div className="p-4 border-t border-border glass">
          {files.length > 0 && (
            <div className="mb-4">
              <FileUpload
                onFileSelect={handleFileSelect}
                files={files}
                onRemoveFile={handleRemoveFile}
              />
            </div>
          )}
          <div className="flex gap-4">
            <Input
              placeholder="Posez votre question juridique..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1"
            />
            <Button onClick={handleSend} className="shrink-0">
              <Send className="h-4 w-4 mr-2" />
              Envoyer
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;