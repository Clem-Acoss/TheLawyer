import React from "react";
import { NewConversationDialog } from "@/components/NewConversationDialog";
import { ConfirmDialog } from "@/components/ConfirmDialog";
import { ErrorModal } from "@/components/errorModal";

type ModalWrapperProps = {
  newConvDialogOpen: boolean;
  setNewConvDialogOpen: (open: boolean) => void;
  onCreateConversation: (title: string) => Promise<void>;


  showConfirm: boolean;
  setShowConfirm: (open: boolean) => void;
  onConfirmDelete: () => void;

  showErrorModal: boolean;
  setShowErrorModal: (open: boolean) => void;
  errorMessage: string | null;
};

export const ModalWrapper: React.FC<ModalWrapperProps> = ({
  newConvDialogOpen,
  setNewConvDialogOpen,
  onCreateConversation,
  showConfirm,
  setShowConfirm,
  onConfirmDelete,
  showErrorModal,
  setShowErrorModal,
  errorMessage,
}) => {
  return (
    <>
      <NewConversationDialog
        open={newConvDialogOpen}
        onOpenChange={setNewConvDialogOpen}
        onCreate={onCreateConversation}
      />
      <ConfirmDialog
        open={showConfirm}
        title="Supprimer la conversation"
        description="Voulez-vous vraiment supprimer cette conversation ?"
        onConfirm={onConfirmDelete}
        onCancel={() => setShowConfirm(false)}
      />
      <ErrorModal
        open={showErrorModal}
        onClose={() => setShowErrorModal(false)}
        description={errorMessage || "Une erreur est survenue."}
      />
    </>
  );
};
