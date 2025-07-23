/**
 * FileUpload.tsx
 * 
 * Composant React permettant à l'utilisateur de téléverser des fichiers.
 * - Prise en charge du glisser-déposer (drag-and-drop) via `react-dropzone`.
 * - Affiche les fichiers sélectionnés et permet leur suppression.
 * - Gère plusieurs types de fichiers : PDF, Word (DOC/DOCX), images (JPG/PNG).
 * 
 * Props :
 * - onFileSelect (function) : callback déclenché lors de la sélection ou du drop de fichiers.
 * - files (File[]) : liste des fichiers actuellement sélectionnés.
 * - onRemoveFile (function) : fonction appelée pour retirer un fichier de la liste.
 * 
 * Utilise :
 * - `react-dropzone` pour la gestion des fichiers en drag-and-drop.
 * - Icônes `Upload` et `X` depuis `lucide-react`.
 * - Composant UI personnalisé `Button`.
 * 
 * Auteur : Clément Gardair
 * Projet : PROJET-DROIT-IA-V2
 */





import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FileUploadProps {
  onFileSelect: (files: File[]) => void;
  files: File[];
  onRemoveFile: (name: string) => void;
}

export const FileUpload = ({ onFileSelect, files, onRemoveFile }: FileUploadProps) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    onFileSelect(acceptedFiles);
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    }
  });

  return (
    <div className="w-full space-y-4">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors
          ${isDragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/20'}`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-8 w-8 mb-4 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          {isDragActive
            ? "Déposez les fichiers ici..."
            : "Glissez-déposez vos fichiers ici, ou cliquez pour sélectionner"}
        </p>
        <p className="text-xs text-muted-foreground mt-2">
          Formats acceptés: PDF, DOC, DOCX, JPG, PNG
        </p>
      </div>

      {files.length > 0 && (
        <div className="space-y-2">
          {files.map((file) => (
            <div key={file.name} className="flex items-center justify-between p-2 glass rounded-lg">
              <span className="text-sm truncate">{file.name}</span>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onRemoveFile(file.name)}
                className="h-8 w-8"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
