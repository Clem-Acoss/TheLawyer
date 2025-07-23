import { useState } from "react";
import { Header } from "@/components/layout/Header";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { TradingChart } from "@/components/dashboard/TradingChart";
import { OrderHistory } from "@/components/dashboard/OrderHistory";
import { BotStatus } from "@/components/dashboard/BotStatus";
import { DollarSign, TrendingUp, Activity, Bot } from "lucide-react";

// Mock data
const mockChartData = [
  { time: '09:00', price: 175.32 },
  { time: '10:00', price: 176.15 },
  { time: '11:00', price: 174.89 },
  { time: '12:00', price: 177.45 },
  { time: '13:00', price: 178.92 },
  { time: '14:00', price: 176.78 },
  { time: '15:00', price: 179.31 },
  { time: '16:00', price: 180.15 },
];

const mockOrders = [
  {
    id: '1',
    symbol: 'AAPL',
    type: 'BUY' as const,
    amount: 10,
    price: 175.32,
    timestamp: '10:30',
    status: 'EXECUTED' as const,
  },
  {
    id: '2',
    symbol: 'AAPL',
    type: 'SELL' as const,
    amount: 5,
    price: 178.92,
    timestamp: '13:15',
    status: 'EXECUTED' as const,
  },
  {
    id: '3',
    symbol: 'TSLA',
    type: 'BUY' as const,
    amount: 3,
    price: 245.67,
    timestamp: '14:20',
    status: 'PENDING' as const,
  },
];

export default function Dashboard() {
  const [botActive, setBotActive] = useState(true);
  const [user] = useState({ name: 'John Doe', email: 'john@example.com' });

  const handleLogout = () => {
    console.log('Logout clicked');
  };

  const handleBotToggle = (active: boolean) => {
    setBotActive(active);
  };

  const handleChartRefresh = () => {
    console.log('Chart refresh clicked');
  };

  return (
    <div className="min-h-screen bg-background">
      <Header user={user} onLogout={handleLogout} />
      
      <main className="container mx-auto px-6 py-8 animate-fade-in">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Valeur du portefeuille"
            value="$12,345.67"
            change="+2.5%"
            isPositive={true}
            icon={<DollarSign className="w-4 h-4 text-primary" />}
            description="depuis hier"
          />
          
          <StatsCard
            title="P&L Journalier"
            value="$234.56"
            change="+12.3%"
            isPositive={true}
            icon={<TrendingUp className="w-4 h-4 text-success" />}
            description="aujourd'hui"
          />
          
          <StatsCard
            title="Trades actifs"
            value="3"
            icon={<Activity className="w-4 h-4 text-warning" />}
          />
          
          <StatsCard
            title="Bot Performance"
            value="87.5%"
            change="+5.2%"
            isPositive={true}
            icon={<Bot className="w-4 h-4 text-primary" />}
            description="taux de réussite"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Trading Chart - Takes 2 columns */}
          <div className="lg:col-span-2">
            <TradingChart
              symbol="AAPL"
              price={180.15}
              change={2.76}
              data={mockChartData}
              onRefresh={handleChartRefresh}
            />
          </div>

          {/* Bot Status */}
          <div>
            <BotStatus
              isActive={botActive}
              onToggle={handleBotToggle}
              strategy="Moving Average (10/50)"
              profit24h={234.56}
              totalTrades={147}
            />
          </div>

          {/* Order History - Full width */}
          <div className="lg:col-span-3">
            <OrderHistory orders={mockOrders} />
          </div>
        </div>
      </main>
    </div>
  );
}