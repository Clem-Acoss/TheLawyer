
import { Button } from "@/components/ui/button";
import { useState } from "react";

export const FloatingButtons = () => {
  const [active, setActive] = useState<string | null>(null);

  const handleClick = (action: string) => {
    setActive(action === active ? null : action); // toggle
  };

  return (
    <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-50 flex gap-2 backdrop-blur-md bg-white/40 border border-gray-200 px-4 py-2 rounded-xl shadow-md">
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${active === "analyse" ? "bg-muted" : ""}`}
        onClick={() => handleClick("analyse")}
      >
        🧠 Analyse
      </Button>
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${active === "x1" ? "bg-muted" : ""}`}
        onClick={() => handleClick("x1")}
      >
        🔁 x1
      </Button>
      <Button
        variant="ghost"
        className={`gap-2 text-sm ${active === "x2" ? "bg-muted" : ""}`}
        onClick={() => handleClick("x2")}
      >
        ✨ x2
      </Button>
    </div>
  );
};
