import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Bot, Activity, Zap, Settings } from "lucide-react";

interface BotStatusProps {
  isActive: boolean;
  onToggle: (active: boolean) => void;
  strategy: string;
  profit24h: number;
  totalTrades: number;
}

export function BotStatus({ 
  isActive, 
  onToggle, 
  strategy, 
  profit24h, 
  totalTrades 
}: BotStatusProps) {
  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
              isActive ? 'bg-success-light' : 'bg-muted'
            }`}>
              <Bot className={`w-5 h-5 ${
                isActive ? 'text-success' : 'text-muted-foreground'
              }`} />
            </div>
            <div>
              <CardTitle>Bot de Trading</CardTitle>
              <Badge 
                variant={isActive ? "default" : "secondary"}
                className={isActive ? "bg-success text-success-foreground" : ""}
              >
                {isActive ? 'ACTIF' : 'INACTIF'}
              </Badge>
            </div>
          </div>
          
          <Switch 
            checked={isActive}
            onCheckedChange={onToggle}
          />
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Activity className="w-4 h-4" />
              Profit 24h
            </div>
            <div className={`text-lg font-semibold ${
              profit24h >= 0 ? 'text-success' : 'text-danger'
            }`}>
              {profit24h >= 0 ? '+' : ''}${profit24h.toFixed(2)}
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Zap className="w-4 h-4" />
              Trades total
            </div>
            <div className="text-lg font-semibold">
              {totalTrades}
            </div>
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="text-sm text-muted-foreground">Stratégie active</div>
          <div className="flex items-center justify-between">
            <span className="font-medium">{strategy}</span>
            <Button variant="outline" size="sm">
              <Settings className="w-4 h-4 mr-2" />
              Configurer
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}