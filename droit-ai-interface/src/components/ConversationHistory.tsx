
/**
 * ConversationHistory.tsx
 * 
 * Composant React affichant l'historique des conversations dans la barre latérale.
 * - Permet de sélectionner une conversation existante via un bouton stylisé.
 * - Permet de supprimer une conversation avec une icône de corbeille.
 * - Met en surbrillance la conversation actuellement sélectionnée.
 * 
 * Props :
 * - conversations (Array<{ title: string, date: string }>) : liste des titres et dates des conversations.
 * - onSelect (function) : fonction appelée lors de la sélection d'une conversation.
 * - onDelete (function) : fonction appelée lors de la suppression d'une conversation.
 * - selectedTitle (string, optionnel) : titre de la conversation actuellement active.
 * 
 * Utilise :
 * - Icônes `MessageSquare` et `Trash2` depuis `lucide-react`.
 * - Composants UI personnalisés `Button` et `ScrollArea`.
 * 
 * Auteur : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */


/**
 * ConversationHistory.tsx
 * 
 * Composant React affichant l'historique des conversations dans la barre latérale.
 * - Permet de sélectionner une conversation existante via un bouton stylisé.
 * - Permet de supprimer une conversation avec une icône de corbeille.
 * - Met en surbrillance la conversation actuellement sélectionnée.
 * - Affiche les boutons Paramètres et Déconnexion en haut.
 * 
 * Props :
 * - conversations (Array<{ title: string, date: string }>) : liste des titres et dates des conversations.
 * - onSelect (function) : fonction appelée lors de la sélection d'une conversation.
 * - onDelete (function) : fonction appelée lors de la suppression d'une conversation.
 * - onLogout (function) : fonction appelée lors du clic sur Déconnexion.
 * - onSettings (function) : fonction appelée lors du clic sur Paramètres.
 * - selectedTitle (string, optionnel) : titre de la conversation actuellement active.
 * 
 * Utilise :
 * - Icônes `MessageSquare`, `Trash2`, `Settings`, `LogOut` depuis `lucide-react`.
 * - Composants UI personnalisés `Button` et `ScrollArea`.
 * 
 * Auteur : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */

import { MessageSquare, Trash2, Settings, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

export interface ConversationHistoryProps {
  conversations: { title: string; date: string }[];
  onSelect: (title: string) => void;
  onDelete: (title: string) => void;
  onLogout: () => void;
  onSettings: () => void;
  selectedTitle?: string;
}

export const ConversationHistory = ({
  conversations,
  onSelect,
  onDelete,
  onLogout,
  onSettings,
  selectedTitle,
}: ConversationHistoryProps) => {
  return (
    <ScrollArea className="flex-1">
      <div className="space-y-2 p-2">
        {/* 🔘 Boutons Paramètres et Déconnexion */}
        <div className="flex justify-between items-center pb-2 border-b mb-2">
          <Button
            variant="ghost"
            className="flex items-center gap-2 text-sm"
            onClick={onSettings}
          >
            <Settings className="w-4 h-4" />
            Paramètres
          </Button>
          <Button
            variant="ghost"
            className="flex items-center gap-2 text-sm text-red-600"
            onClick={onLogout}
          >
            <LogOut className="w-4 h-4" />
            Déconnexion
          </Button>
        </div>

        {/* 📜 Liste des conversations */}
        {conversations.length === 0 && (
          <p className="text-center text-muted-foreground">Aucune conversation disponible</p>
        )}

        {conversations.map(({ title, date }) => (
          <div key={title} className="flex items-center justify-between">
            <Button
              variant={selectedTitle === title ? 'secondary' : 'ghost'}
              className="flex-1 justify-start gap-2"
              onClick={() => onSelect(title)}
            >
              <MessageSquare className="h-4 w-4" />
              <div className="flex-1 truncate text-left">
                <span className="text-sm">{title}</span>
                <span className="block text-xs text-muted-foreground">{date}</span>
              </div>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="ml-2"
              onClick={() => onDelete(title)}
            >
              <Trash2 className="h-4 w-4 text-red-500 hover:text-red-700" />
            </Button>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
};
