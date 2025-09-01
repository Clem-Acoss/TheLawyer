
import { Button } from "@/components/ui/button";
import { useState } from "react";


type FloatingButtonsProps = {
  currentSource: "urssaf" | "lamy" | "legifrance" | "boss";
  onSelectSource: (src: "urssaf" | "lamy" | "legifrance" | "boss") => void;
};

export const FloatingButtons: React.FC<FloatingButtonsProps> = ({ currentSource, onSelectSource }) => {
  return (
    <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-50 flex gap-2 backdrop-blur-md bg-white/40 border border-gray-200 px-4 py-2 rounded-xl shadow-md">
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${currentSource === "urssaf" ? "bg-muted" : ""}`}
        onClick={() => onSelectSource("urssaf")}
      >
        🏢 URSSAF
      </Button>
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${currentSource === "lamy" ? "bg-muted" : ""}`}
        onClick={() => onSelectSource("lamy")}
      >
        📚 LAMY
      </Button>
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${currentSource === "legifrance" ? "bg-muted" : ""}`}
        onClick={() => onSelectSource("legifrance")}
      >
        ⚖️ Legifrance
      </Button>
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${currentSource === "boss" ? "bg-muted" : ""}`}
        onClick={() => onSelectSource("boss")}
      >
        🧑‍💼 BOSS
      </Button>
    </div>
  );
};
