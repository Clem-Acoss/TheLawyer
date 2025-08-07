import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FileText, Send, ChevronDown } from "lucide-react";
import { FileUpload } from "@/components/FileUpload";

type InputAreaProps = {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  isLoading: boolean;
  showUpload: boolean;
  toggleUpload: () => void;
  files: File[];
  onFileSelect: (files: File[]) => void;
  onRemoveFile: (name: string) => void;
  toggleFloatingButtons: () => void;
};

export const InputArea = ({
  input,
  onInputChange,
  onSend,
  isLoading,
  showUpload,
  toggleUpload,
  files,
  onFileSelect,
  onRemoveFile,
  toggleFloatingButtons,
}: InputAreaProps) => (
  <div className="p-4 border-t border-border glass flex flex-col gap-2">
    {showUpload && (
      <FileUpload files={files} onFileSelect={onFileSelect} onRemoveFile={onRemoveFile} />
    )}
    <div className="flex items-center gap-2">
      <Input
        placeholder="Posez votre question..."
        value={input}
        onChange={onInputChange}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        disabled={isLoading}
      />
      <Button
        variant={showUpload ? "default" : "outline"}
        size="icon"
        onClick={toggleUpload}
        title="Importer un PDF"
      >
        <FileText className="h-5 w-5" />
      </Button>
      <Button variant="outline" size="icon" onClick={toggleFloatingButtons}>
        <ChevronDown className="h-4 w-4" />
      </Button>
      <Button onClick={onSend} disabled={isLoading} size="icon">
        <Send />
      </Button>
    </div>
  </div>
);
