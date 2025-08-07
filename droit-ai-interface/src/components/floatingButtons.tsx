import { Button } from "@/components/ui/button";

export const FloatingButtons = () => (
  <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-50 flex gap-2 backdrop-blur-sm bg-background/80 px-4 py-2 rounded-xl shadow-md">
    <Button variant="ghost" className="gap-2 text-sm">
      🧠 Analyse
    </Button>
    <Button variant="ghost" className="gap-2 text-sm">
      🔁 x1
    </Button>
    <Button variant="ghost" className="gap-2 text-sm">
      ✨ x2
    </Button>
  </div>
);
