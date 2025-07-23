import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  title: string;
  value: string;
  change?: string;
  isPositive?: boolean;
  icon: ReactNode;
  description?: string;
}

export function StatsCard({ 
  title, 
  value, 
  change, 
  isPositive, 
  icon, 
  description 
}: StatsCardProps) {
  return (
    <Card className="glass-card hover:shadow-medium transition-all duration-300">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
          {icon}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold mb-1">{value}</div>
        {change && (
          <p className={cn(
            "text-xs flex items-center gap-1",
            isPositive ? "text-success" : "text-danger"
          )}>
            <span className={cn(
              "px-1.5 py-0.5 rounded text-xs font-medium",
              isPositive ? "bg-success-light" : "bg-danger-light"
            )}>
              {change}
            </span>
            {description}
          </p>
        )}
      </CardContent>
    </Card>
  );
}