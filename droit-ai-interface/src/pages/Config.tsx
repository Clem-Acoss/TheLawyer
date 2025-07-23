import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "@/components/config/Header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { Settings, TrendingUp, Shield, DollarSign, Target } from "lucide-react";

interface BotConfig {
  isActive: boolean;
  strategy: string;
  profitThreshold: string;
  stopLoss: string;
  maxAmount: string;
  symbols: string;
}

const Config = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [config, setConfig] = useState<BotConfig>({
    isActive: false,
    strategy: "",
    profitThreshold: "",
    stopLoss: "",
    maxAmount: "",
    symbols: "BTC/USDT"
  });

  const [errors, setErrors] = useState<Partial<BotConfig>>({});

  const strategies = [
    { value: "moving_average", label: "Moving Average" },
    { value: "rsi", label: "RSI (Relative Strength Index)" },
    { value: "macd", label: "MACD" },
    { value: "bollinger_bands", label: "Bollinger Bands" },
    { value: "scalping", label: "Scalping" }
  ];

  const validateForm = (): boolean => {
    const newErrors: Partial<BotConfig> = {};

    if (!config.strategy) {
      newErrors.strategy = "Veuillez sélectionner une stratégie";
    }

    if (!config.profitThreshold || parseFloat(config.profitThreshold) <= 0) {
      newErrors.profitThreshold = "Seuil de profit requis (> 0)";
    }

    if (!config.stopLoss || parseFloat(config.stopLoss) <= 0) {
      newErrors.stopLoss = "Stop loss requis (> 0)";
    }

    if (!config.maxAmount || parseFloat(config.maxAmount) <= 0) {
      newErrors.maxAmount = "Montant maximum requis (> 0)";
    }

    if (!config.symbols.trim()) {
      newErrors.symbols = "Au moins un symbole requis";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast({
        title: "Erreur de validation",
        description: "Veuillez corriger les erreurs du formulaire",
        variant: "destructive"
      });
      return;
    }

    console.log("Configuration du bot sauvegardée:", {
      ...config,
      profitThreshold: parseFloat(config.profitThreshold),
      stopLoss: parseFloat(config.stopLoss),
      maxAmount: parseFloat(config.maxAmount),
      symbols: config.symbols.split(",").map(s => s.trim())
    });

    toast({
      title: "Configuration sauvegardée",
      description: "Les paramètres du bot ont été mis à jour avec succès",
      variant: "default"
    });
  };

  const handleCancel = () => {
    setConfig({
      isActive: false,
      strategy: "",
      profitThreshold: "",
      stopLoss: "",
      maxAmount: "",
      symbols: "BTC/USDT"
    });
    setErrors({});
    
    toast({
      title: "Modifications annulées",
      description: "Le formulaire a été réinitialisé",
      variant: "default"
    });
  };

  const handleBackToDashboard = () => {
    navigate("/dashboard");
  };

  const user = {
    name: "John Trader",
    email: "john@tradingbot.com"
  };

  const handleLogout = () => {
    console.log("Logout");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background">
      <Header 
        user={user}
        onLogout={handleLogout}
        showBackButton={true}
        onBack={handleBackToDashboard}
        title="Configuration du Bot"
      />
      
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                <Settings className="h-5 w-5 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Configuration du Bot de Trading</h1>
                <p className="text-muted-foreground">Configurez les paramètres de votre bot automatisé</p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Activation du Bot */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-success" />
                  Activation du Bot
                </CardTitle>
                <CardDescription>
                  Activez ou désactivez le trading automatique
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-2">
                  <Switch
                    id="bot-active"
                    checked={config.isActive}
                    onCheckedChange={(checked) => 
                      setConfig(prev => ({ ...prev, isActive: checked }))
                    }
                  />
                  <Label htmlFor="bot-active" className="text-sm font-medium">
                    {config.isActive ? "Bot activé" : "Bot désactivé"}
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Quand activé, le bot exécutera automatiquement les trades selon la stratégie configurée
                </p>
              </CardContent>
            </Card>

            {/* Stratégie de Trading */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Stratégie de Trading
                </CardTitle>
                <CardDescription>
                  Sélectionnez l'algorithme de trading à utiliser
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="strategy">Stratégie</Label>
                  <Select
                    value={config.strategy}
                    onValueChange={(value) => {
                      setConfig(prev => ({ ...prev, strategy: value }));
                      setErrors(prev => ({ ...prev, strategy: undefined }));
                    }}
                  >
                    <SelectTrigger className={errors.strategy ? "border-danger" : ""}>
                      <SelectValue placeholder="Choisir une stratégie" />
                    </SelectTrigger>
                    <SelectContent>
                      {strategies.map((strategy) => (
                        <SelectItem key={strategy.value} value={strategy.value}>
                          {strategy.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.strategy && (
                    <p className="text-xs text-danger mt-1">{errors.strategy}</p>
                  )}
                  <p className="text-xs text-muted-foreground mt-1">
                    Chaque stratégie utilise des indicateurs techniques différents pour prendre des décisions
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Paramètres de Risque */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-warning" />
                  Gestion des Risques
                </CardTitle>
                <CardDescription>
                  Configurez les seuils de profit et de perte
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="profit-threshold">Seuil de prise de profit (%)</Label>
                    <Input
                      id="profit-threshold"
                      type="number"
                      step="0.1"
                      placeholder="ex: 2.5"
                      value={config.profitThreshold}
                      onChange={(e) => {
                        setConfig(prev => ({ ...prev, profitThreshold: e.target.value }));
                        setErrors(prev => ({ ...prev, profitThreshold: undefined }));
                      }}
                      className={errors.profitThreshold ? "border-danger" : ""}
                    />
                    {errors.profitThreshold && (
                      <p className="text-xs text-danger mt-1">{errors.profitThreshold}</p>
                    )}
                    <p className="text-xs text-muted-foreground mt-1">
                      Le bot vendra automatiquement quand ce profit est atteint
                    </p>
                  </div>

                  <div>
                    <Label htmlFor="stop-loss">Seuil de stop loss (%)</Label>
                    <Input
                      id="stop-loss"
                      type="number"
                      step="0.1"
                      placeholder="ex: 1.5"
                      value={config.stopLoss}
                      onChange={(e) => {
                        setConfig(prev => ({ ...prev, stopLoss: e.target.value }));
                        setErrors(prev => ({ ...prev, stopLoss: undefined }));
                      }}
                      className={errors.stopLoss ? "border-danger" : ""}
                    />
                    {errors.stopLoss && (
                      <p className="text-xs text-danger mt-1">{errors.stopLoss}</p>
                    )}
                    <p className="text-xs text-muted-foreground mt-1">
                      Le bot vendra automatiquement pour limiter les pertes
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Paramètres de Trading */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-success" />
                  Paramètres de Trading
                </CardTitle>
                <CardDescription>
                  Configurez les montants et symboles à trader
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="max-amount">Montant maximum par trade (USDT)</Label>
                  <Input
                    id="max-amount"
                    type="number"
                    step="1"
                    placeholder="ex: 100"
                    value={config.maxAmount}
                    onChange={(e) => {
                      setConfig(prev => ({ ...prev, maxAmount: e.target.value }));
                      setErrors(prev => ({ ...prev, maxAmount: undefined }));
                    }}
                    className={errors.maxAmount ? "border-danger" : ""}
                  />
                  {errors.maxAmount && (
                    <p className="text-xs text-danger mt-1">{errors.maxAmount}</p>
                  )}
                  <p className="text-xs text-muted-foreground mt-1">
                    Montant maximum que le bot peut utiliser par transaction
                  </p>
                </div>

                <div>
                  <Label htmlFor="symbols">Symboles tradés</Label>
                  <Input
                    id="symbols"
                    placeholder="ex: BTC/USDT, ETH/USDT, ADA/USDT"
                    value={config.symbols}
                    onChange={(e) => {
                      setConfig(prev => ({ ...prev, symbols: e.target.value }));
                      setErrors(prev => ({ ...prev, symbols: undefined }));
                    }}
                    className={errors.symbols ? "border-danger" : ""}
                  />
                  {errors.symbols && (
                    <p className="text-xs text-danger mt-1">{errors.symbols}</p>
                  )}
                  <p className="text-xs text-muted-foreground mt-1">
                    Paires de trading séparées par des virgules (format: BASE/QUOTE)
                  </p>
                </div>
              </CardContent>
            </Card>

            <Separator />

            {/* Boutons d'action */}
            <div className="flex flex-col sm:flex-row gap-4 justify-end">
              <Button 
                type="button" 
                variant="outline" 
                onClick={handleCancel}
                className="sm:order-1"
              >
                Annuler
              </Button>
              
              <Button 
                type="button" 
                variant="secondary" 
                onClick={handleBackToDashboard}
                className="sm:order-2"
              >
                Retour au Dashboard
              </Button>
              
              <Button 
                type="submit" 
                variant="success"
                className="sm:order-3"
              >
                Enregistrer la configuration
              </Button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default Config;