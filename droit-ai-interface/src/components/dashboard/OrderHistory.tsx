import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, Clock } from "lucide-react";

interface Order {
  id: string;
  symbol: string;
  type: 'BUY' | 'SELL';
  amount: number;
  price: number;
  timestamp: string;
  status: 'EXECUTED' | 'PENDING' | 'CANCELLED';
}

interface OrderHistoryProps {
  orders: Order[];
}

export function OrderHistory({ orders }: OrderHistoryProps) {
  const getStatusColor = (status: Order['status']) => {
    switch (status) {
      case 'EXECUTED':
        return 'bg-success text-success-foreground';
      case 'PENDING':
        return 'bg-warning text-warning-foreground';
      case 'CANCELLED':
        return 'bg-muted text-muted-foreground';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Historique des ordres</CardTitle>
          <Button variant="outline" size="sm">
            Voir tout
          </Button>
        </div>
      </CardHeader>
      
      <CardContent>
        <ScrollArea className="h-80">
          <div className="space-y-3">
            {orders.map((order) => (
              <div 
                key={order.id}
                className="flex items-center justify-between p-3 rounded-lg border border-border/50 hover:bg-muted/30 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    order.type === 'BUY' ? 'bg-success-light' : 'bg-danger-light'
                  }`}>
                    {order.type === 'BUY' ? (
                      <TrendingUp className="w-4 h-4 text-success" />
                    ) : (
                      <TrendingDown className="w-4 h-4 text-danger" />
                    )}
                  </div>
                  
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{order.symbol}</span>
                      <Badge 
                        variant="outline"
                        className={order.type === 'BUY' ? 'text-success border-success' : 'text-danger border-danger'}
                      >
                        {order.type}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      {order.timestamp}
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="font-medium">
                    {order.amount} @ ${order.price.toFixed(2)}
                  </div>
                  <Badge className={getStatusColor(order.status)}>
                    {order.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}