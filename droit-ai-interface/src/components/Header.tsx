import React from "react";
import { Button } from "@/components/ui/button";
import { Menu, ChevronDown } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import { ConversationHistory } from "@/components/ConversationHistory";

type HeaderProps = {
  convForHistory: any[];
  selectedTitle?: string;
  onSelect: (title: string) => void;
  onDelete: (title: string) => void;
  onSettings: () => void;
  onLogout: () => void;
  onNewConversation: () => void;
};

export const Header = ({
  convForHistory,
  selectedTitle,
  onSelect,
  onDelete,
  onSettings,
  onLogout,
  onNewConversation,
}: HeaderProps) => (
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
          <Button variant="outline" className="mb-4" onClick={onNewConversation}>
            Nouvelle conversation
          </Button>
          <ConversationHistory
            conversations={convForHistory}
            selectedTitle={selectedTitle}
            onSelect={onSelect}
            onDelete={onDelete}
            onSettings={onSettings}
            onLogout={onLogout}
            
          />
        </div>
      </SheetContent>
    </Sheet>
    <h1 className="text-lg font-semibold ml-4">Assistant Juridique</h1>
  </header>
);
