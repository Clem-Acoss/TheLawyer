import { useState } from 'react';
import { Button } from '@/components/ui/button';  // Importation de ton composant Button

interface NewConversationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (title: string) => void;
}

export const NewConversationModal = ({ isOpen, onClose, onCreate }: NewConversationModalProps) => {
  const [title, setTitle] = useState("");

  const handleSubmit = () => {
    if (title.trim()) {
      onCreate(title);  // Appelle la fonction onCreate avec le titre
      setTitle("");      // Réinitialiser le champ de titre
      onClose();         // Fermer la modale après création
    }
  };

  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-card p-6 rounded-lg shadow-lg w-full sm:w-96">
            <h2 className="text-lg font-semibold text-primary mb-4">Nouvelle Conversation</h2>
            <input
              className="w-full p-3 rounded-lg border border-input focus:outline-none focus:ring-2 focus:ring-primary text-black"  // Ajout de text-black ici
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Entrez le titre de la conversation"
            />
            <div className="mt-4 flex justify-end space-x-2">
              <Button variant="ghost" onClick={onClose}>Annuler</Button>
              <Button onClick={handleSubmit}>Créer</Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
