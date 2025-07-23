import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, RefreshCw } from "lucide-react";

interface TradingChartProps {
  symbol: string;
  price: number;
  change: number;
  data: Array<{ time: string; price: number }>;
  isLoading?: boolean;
  onRefresh?: () => void;
}

export function TradingChart({ 
  symbol, 
  price, 
  change, 
  data, 
  isLoading,
  onRefresh 
}: TradingChartProps) {
  const isPositive = change >= 0;

  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CardTitle className="text-xl">{symbol}</CardTitle>
            <Badge 
              variant={isPositive ? "default" : "destructive"}
              className={isPositive ? "bg-success text-success-foreground" : ""}
            >
              {isPositive ? (
                <TrendingUp className="w-3 h-3 mr-1" />
              ) : (
                <TrendingDown className="w-3 h-3 mr-1" />
              )}
              {isPositive ? '+' : ''}{change.toFixed(2)}%
            </Badge>
          </div>
          
          <Button 
            variant="ghost" 
            size="icon"
            onClick={onRefresh}
            disabled={isLoading}
            className="rounded-full"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        
        <div className="text-3xl font-bold">
          ${price.toFixed(2)}
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="time" 
                axisLine={false}
                tickLine={false}
                className="text-xs"
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                className="text-xs"
                domain={['dataMin - 1', 'dataMax + 1']}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '0.75rem',
                  boxShadow: 'var(--shadow-medium)'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke={isPositive ? "hsl(var(--success))" : "hsl(var(--danger))"}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: isPositive ? "hsl(var(--success))" : "hsl(var(--danger))" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}