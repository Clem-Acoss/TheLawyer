import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import React, { useState } from "react";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreate: (title: string) => Promise<void>;
};

export const NewConversationDialog = ({ open, onOpenChange, onCreate }: Props) => {
  const [title, setTitle] = useState("");

  const handleCancel = () => {
    setTitle("");
    onOpenChange(false);
  };

  const handleCreate = async () => {
    await onCreate(title || "Nouvelle conversation");
    setTitle("");
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={(open) => {
      if (!open) handleCancel();
    }}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nouvelle conversation</DialogTitle>
        </DialogHeader>
        <Input
          placeholder="Titre de la conversation"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <DialogFooter>
          <Button variant="outline" onClick={handleCancel}>
            Annuler
          </Button>
          <Button onClick={handleCreate}>
            Créer
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
