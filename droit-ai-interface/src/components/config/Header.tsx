import { Button } from "@/components/ui/button";
import { User, LogOut, ArrowLeft } from "lucide-react";

interface HeaderProps {
  user?: {
    name: string;
    email: string;
  };
  onLogout?: () => void;
  showBackButton?: boolean;
  onBack?: () => void;
  title?: string;
}

const Header = ({ 
  user = { name: "Trader", email: "trader@example.com" }, 
  onLogout = () => console.log("Logout clicked"),
  showBackButton = false,
  onBack = () => window.history.back(),
  title = "Trading Bot"
}: HeaderProps) => {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {showBackButton && (
              <Button 
                variant="ghost" 
                size="icon"
                onClick={onBack}
                className="hover:bg-accent"
              >
                <ArrowLeft className="h-4 w-4" />
              </Button>
            )}
            <div>
              <h1 className="text-xl font-bold text-foreground">{title}</h1>
              <p className="text-sm text-muted-foreground">Gestion automatisée</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <User className="h-4 w-4 text-primary" />
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-foreground">{user.name}</p>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </div>
            
            <Button 
              variant="ghost" 
              size="sm"
              onClick={onLogout}
              className="text-muted-foreground hover:text-foreground"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Déconnexion
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;