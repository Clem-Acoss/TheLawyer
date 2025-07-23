import { Bell, Settings, LogOut, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  user?: { name: string; email: string };
  onLogout?: () => void;
}

export function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="glass-card border-b-0 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <TrendingUp className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-xl font-semibold">TradeFlow</h1>
      </div>

      {user && (
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" className="rounded-full">
            <Bell className="w-5 h-5" />
          </Button>
          
          <Button variant="ghost" size="icon" className="rounded-full">
            <Settings className="w-5 h-5" />
          </Button>

          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-sm font-medium">{user.name}</p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
            </div>
            
            <Button 
              variant="ghost" 
              size="icon" 
              className="rounded-full"
              onClick={onLogout}
            >
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}