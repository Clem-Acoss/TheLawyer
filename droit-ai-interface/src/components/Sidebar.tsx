import React from "react";
import { Button } from "@/components/ui/button";
import { ConversationHistory } from "@/components/ConversationHistory";

type SidebarProps = {
  conversations: any[];
  selectedTitle?: string;
  onSelect: (title: string) => void;
  onDelete: (title: string) => void;
  onSettings: () => void;
  onLogout: () => void;
  onCraClick: () => void;
  onNewConversation: () => void;
};

export const Sidebar = ({
  conversations,
  selectedTitle,
  onSelect,
  onDelete,
  onSettings,
  onLogout,
  onCraClick,
  onNewConversation,
}: SidebarProps) => (
  <aside className="hidden md:flex w-80 border-r border-border flex-col p-4">
    <Button variant="outline" className="mb-4 w-full" onClick={onNewConversation}>
      Nouvelle conversation
    </Button>
    <ConversationHistory
      conversations={conversations}
      selectedTitle={selectedTitle}
      onSelect={onSelect}
      onDelete={onDelete}
      onSettings={onSettings}
      onLogout={onLogout}
      
    />
    {conversations.length === 0 && <p>Aucune conversation disponible</p>}
  </aside>
);
