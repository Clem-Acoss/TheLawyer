
/**
 * pages/index.tsx
 * 
 * Composant principal de l'application React - Assistant Juridique.
 * 
 * Fonctionnalités principales :
 * - Gestion des conversations avec l'assistant juridique, incluant la sélection, la création, 
 *   la suppression et l'historique des conversations.
 * - Interface utilisateur responsive avec une sidebar pour la gestion des conversations sur grand écran 
 *   et un panneau latéral (Sheet) pour les écrans mobiles.
 * - Envoi de messages texte et upload de fichiers PDF en lien avec une conversation sélectionnée.
 * - Support de deux modes d'interaction avec le backend : 
 *    - RAG (Retrieval-Augmented Generation) pour la recherche assistée par documents.
 *    - LLM simple pour un chatbot basé uniquement sur un modèle de langage.
 * - Gestion de l'authentification via token JWT stocké dans le localStorage.
 * - Scroll automatique vers le dernier message lors de l'ajout de nouveaux messages.
 * - Utilisation de composants UI personnalisés (Button, Input, ScrollArea, DropdownMenu, etc.) 
 *   pour une expérience utilisateur fluide et cohérente.
 * 
 * Types utilisés :
 * - Conversation : identifiant, titre, date de création.
 * - MessageFromAPI : contenu et émetteur du message.
 * - Message : structure complète d'un message avec ID, émetteur, contenu, date.
 * - ApiResponse : format de réponse attendu du backend, contenant un contenu texte.
 * 
 * Hooks React utilisés :
 * - useState pour la gestion des états locaux (messages, input, fichiers, conversations, mode, etc.).
 * - useEffect pour le chargement initial des conversations et le scroll automatique.
 * - useRef pour le focus automatique sur la fin de la liste des messages.
 * 
 * Auteurs : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */


import React, { useState, useEffect, useRef } from "react";
import { Send, Menu, ChevronDown, FileText } from "lucide-react"; 
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
import { useNavigate } from "react-router-dom";
import { ConfirmDialog } from "@/components/ConfirmDialog";
import { NewConversationDialog } from "@/components/NewConversationDialog";
import { ErrorModal } from "@/components/errorModal";
type Conversation = {
  id: number;
  title: string;
  created_at: string;
};
type MessageFromAPI = {
  content: string;
  sender: string;
};
type Message = {
  id: number;
  sender: string;
  content: string;
  created_at: string;
};
type ApiResponse = {
  content?: string;
  response?: string;
}
const Index = () => {
  const { logout } = useUser();
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [showUpload, setShowUpload] = useState(false);
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
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showErrorModal, setShowErrorModal] = useState(false);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

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
  const showError = (message: string) => {
    setErrorMessage(message);
    setShowErrorModal(true);
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
      showError("Veuillez sélectionner une conversation ou en créer une nouvelle.");
      return;
    }

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    if (userMessage) {
      setMessages((prev) => [...prev, { text: userMessage, isAi: false }]);
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        showError("Vous devez être connecté.");
        setIsLoading(false);
        return;
      }

      if (files.length > 0) {
        // Cas avec PDF à envoyer (uniquement en mode RAG)
        if (mode !== "rag") {
          showError("L'envoi de fichiers PDF n'est disponible qu'en mode RAG.");
          setIsLoading(false);
          return;
        }

        console.log("Envoi de fichier(s) PDF...");
        const formData = new FormData();
        formData.append("conversation_id", String(selectedConvId));
        formData.append("question", userMessage || "");
        formData.append("file", files[0]);

        const response = await fetch("/rag/ask-with-pdf", {
          method: "POST",
          body: formData,
          headers: {
            Authorization: `Bearer ${token}`,
            
          },
        });

        if (!response.ok) throw new Error("Erreur lors de l'envoi du PDF.");

        const data: ApiResponse = await response.json();

        setMessages((prev) => [
          ...prev,
          { text: data.content || data.response || "Réponse reçue.", isAi: true },
        ]);
        setFiles([]);
      } else {
        // Cas sans fichier
        if (mode === "rag") {
          // RAG sans fichier : on utilise ton endpoint RAG classique (ex: /rag/ask)
          const response = await fetch("/rag/ask", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              conversation_id: selectedConvId,
              question: userMessage,
            }),
          });

          if (!response.ok) throw new Error("Erreur lors de la requête RAG.");

          const data: ApiResponse = await response.json();

          setMessages((prev) => [
            ...prev,
            { text: data.content || data.response || "Réponse reçue.", isAi: true },
          ]);
        } else {
          // Mode LLM simple
          const response = await fetch("/chat/send-message-llm", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
            conversation_id: selectedConvId,
            sender: "user",         
            content: userMessage,   
          })

          });

          if (!response.ok) throw new Error("Erreur lors de la requête LLM.");

          const data: ApiResponse = await response.json();

          setMessages((prev) => [
            ...prev,
            { text: data.content || data.response || "Réponse reçue.", isAi: true },
          ]);
        }
      }
    } catch (e) {
      console.error(e);
      showError(`Erreur: ${(e as Error).message}`);
    } finally {
      setIsLoading(false);
    }
  };


  const startNewConversation = () => {
  setNewConvDialogOpen(true);
  };

  const handleNewConversation = async (title: string) => {
    setNewConvDialogOpen(false);
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

  
  const handleDeleteConversation = (title: string) => {
    const conv = conversations.find((c) => c.title === title);
    if (!conv) return;

    setConfirmCallback(() => async () => {
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
      } finally {
        setShowConfirm(false);
      }
    });

    setShowConfirm(true);
  };



  const handleSettings = () => {
    console.log("Ouverture des paramètres");
    
  };

  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); 
    navigate("/login"); 
  };
  const [showConfirm, setShowConfirm] = useState(false);
  const [confirmCallback, setConfirmCallback] = useState<() => void>(() => {});
  const [newConvDialogOpen, setNewConvDialogOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="hidden md:flex w-80 border-r border-border flex-col p-4">
        <Button variant="outline" className="mb-4 w-full" onClick={startNewConversation}>
          Nouvelle conversation
        </Button>
        <ConversationHistory
           conversations={convForHistory}
           selectedTitle={selectedTitle}
           onSelect={handleSelectConversation}
           onDelete={handleDeleteConversation}
           onSettings={handleSettings}    
           onLogout={handleLogout} 
        />
        {conversations.length === 0 && <p>Aucune conversation disponible</p>}
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        {/* Header */}
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
                   selectedTitle={selectedTitle}
                   onSelect={handleSelectConversation}
                   onDelete={handleDeleteConversation}
                   onSettings={handleSettings}    
                   onLogout={handleLogout}    

                />
              </div>
            </SheetContent>
          </Sheet>
          <h1 className="text-lg font-semibold ml-4">Assistant Juridique</h1>
        </header>

        {/* Messages */}
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

        {/* Zone d’input et PDF */}
        <div className="p-4 border-t border-border glass flex flex-col gap-2">
          {/* Affichage conditionnel du FileUpload */}
          {showUpload && (
            <FileUpload
              files={files}
              onFileSelect={setFiles}
              onRemoveFile={(name) =>
                setFiles((prev) => prev.filter((file) => file.name !== name))
              }
            />
          )}

          <div className="flex items-center gap-2">
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

            {/* Bouton d’affichage de la zone d’upload */}
            <Button
              variant={showUpload ? "default" : "outline"}
              size="icon"
              onClick={() => setShowUpload((prev) => !prev)}
              title="Importer un PDF"
            >
              <FileText className="h-5 w-5" />
            </Button>

            {/* Menu déroulant pour RAG/LLM */}
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

            {/* Bouton envoyer */}
            <Button onClick={handleSend} disabled={isLoading} size="icon">
              <Send />
            </Button>
          </div>
        </div>
      </main>
      <NewConversationDialog
         open={newConvDialogOpen}
         onOpenChange={setNewConvDialogOpen}
         onCreate={handleNewConversation}
      />
      <ConfirmDialog
        open={showConfirm}
        title="Supprimer la conversation"
        description="Voulez-vous vraiment supprimer cette conversation ?"
        onConfirm={() => {
          if (confirmCallback) confirmCallback();
        }}
        onCancel={() => setShowConfirm(false)}
      />
      <ErrorModal
        open={showErrorModal}
        onClose={() => setShowErrorModal(false)}
        description={errorMessage || "Une erreur est survenue."}
      />
    </div>
  );
};

export default Index;