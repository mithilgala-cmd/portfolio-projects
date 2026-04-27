"use client";

import TradingChart from "@/components/TradingChart";
import Sidebar from "@/components/Sidebar";
import OrderBook from "@/components/OrderBook";
import { Activity, LayoutDashboard, Settings, Wallet, ArrowUpCircle, ArrowDownCircle, Search, Bell, History, TrendingUp } from "lucide-react";
import { useEffect, useState } from "react";

export default function Home() {
  const [portfolio, setPortfolio] = useState<any>(null);
  const [trades, setTrades] = useState<any[]>([]);
  const [bots, setBots] = useState<any[]>([]);
  const [currentPrice, setCurrentPrice] = useState<number | null>(null);
  const [amount, setAmount] = useState<string>("0.01");

  const fetchData = async () => {
    try {
      const [portRes, tradesRes, botsRes] = await Promise.all([
        fetch("http://localhost:8001/api/portfolio"),
        fetch("http://localhost:8001/api/trades"),
        fetch("http://localhost:8001/api/bots")
      ]);
      
      if (portRes.ok) setPortfolio(await portRes.json());
      if (tradesRes.ok) setTrades(await tradesRes.json());
      if (botsRes.ok) setBots(await botsRes.json());
    } catch (err) {
      console.error("Failed to fetch data:", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const handleTrade = async (type: "buy" | "sell") => {
    if (!currentPrice) return;
    
    try {
      const res = await fetch("http://localhost:8001/api/trade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type,
          symbol: "BTC",
          amount: parseFloat(amount),
          price: currentPrice
        })
      });
      
      const result = await res.json();
      if (result.status === "success") {
        fetchData(); // Refresh data
        // We could add a toast notification here instead of alert
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (err) {
      console.error("Trade failed:", err);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Header */}
        <header className="h-20 border-b border-border bg-panel/20 backdrop-blur-md flex items-center justify-between px-8 relative z-10">
          <div className="flex items-center gap-8">
            <h2 className="text-xl font-bold tracking-tight">Market Overview</h2>
            <div className="hidden lg:flex items-center bg-white/5 border border-border rounded-xl px-4 py-2 gap-3 w-80 focus-within:border-primary transition-colors">
              <Search size={18} className="text-gray-500" />
              <input 
                type="text" 
                placeholder="Search assets, trades, bots..." 
                className="bg-transparent border-none outline-none text-sm w-full"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="hidden md:flex flex-col items-end">
              <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Available Balance</div>
              <div className="font-mono font-black text-lg text-success">
                ${portfolio?.balance_usd?.toLocaleString(undefined, { minimumFractionDigits: 2 }) || "0.00"}
              </div>
            </div>
            
            <div className="flex items-center gap-3 border-l border-border pl-6">
              <button className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 transition-all">
                <Bell size={20} />
              </button>
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center font-bold shadow-lg shadow-primary/20 cursor-pointer">
                MG
              </div>
            </div>
          </div>
        </header>
        
        {/* Dashboard Content */}
        <div className="flex-1 p-6 overflow-y-auto custom-scrollbar">
          <div className="grid grid-cols-12 gap-6 max-w-[1600px] mx-auto">
            
            {/* Left Column: Chart & Trade */}
            <div className="col-span-12 lg:col-span-9 space-y-6">
              
              {/* Trading Chart */}
              <div className="min-h-[500px]">
                <TradingChart onPriceUpdate={(p) => setCurrentPrice(p)} />
              </div>
              
              {/* Bottom Row: Trade Panel & Active Bots */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Trade Panel */}
                <div className="panel flex flex-col gap-6">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold flex items-center gap-2">
                      <TrendingUp size={18} className="text-primary" /> Instant Trade
                    </h3>
                    <div className="flex bg-white/5 p-1 rounded-lg">
                      <button className="px-3 py-1 text-xs font-bold rounded-md bg-primary text-white">Market</button>
                      <button className="px-3 py-1 text-xs font-bold text-gray-500 hover:text-gray-300">Limit</button>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="relative">
                      <label className="absolute top-3 left-4 text-[10px] font-bold text-gray-500 uppercase">Buy/Sell Amount</label>
                      <input 
                        type="number" 
                        value={amount} 
                        onChange={(e) => setAmount(e.target.value)}
                        className="w-full bg-background/50 border border-border rounded-xl px-4 pt-8 pb-3 font-mono text-lg focus:outline-none focus:border-primary transition-all"
                      />
                      <div className="absolute right-4 top-1/2 -translate-y-1/2 mt-2 font-bold text-gray-400">BTC</div>
                    </div>
                    
                    <div className="p-4 bg-white/5 rounded-xl border border-border flex justify-between items-center">
                      <span className="text-sm text-gray-400">Estimated Total</span>
                      <span className="font-mono font-bold text-xl">
                        ${(parseFloat(amount || "0") * (currentPrice || 0)).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <button 
                        onClick={() => handleTrade("buy")}
                        className="bg-success hover:bg-success/90 text-white h-14 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-success/10 active:scale-[0.98]"
                      >
                        <ArrowUpCircle size={20} /> Buy BTC
                      </button>
                      <button 
                        onClick={() => handleTrade("sell")}
                        className="bg-danger hover:bg-danger/90 text-white h-14 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-danger/10 active:scale-[0.98]"
                      >
                        <ArrowDownCircle size={20} /> Sell BTC
                      </button>
                    </div>
                  </div>
                </div>

                {/* Active Bots List */}
                <div className="panel flex flex-col">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-bold flex items-center gap-2">
                      <Settings size={18} className="text-primary" /> Active Trading Bots
                    </h3>
                    <span className="text-[10px] font-bold px-2 py-1 bg-primary/10 text-primary rounded-full">
                      {bots.length} RUNNING
                    </span>
                  </div>
                  <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                    {bots.length > 0 ? (
                      bots.map((bot, i) => (
                        <div key={i} className="p-4 bg-background/40 rounded-xl border border-border group hover:border-primary/30 transition-all">
                          <div className="flex justify-between items-center mb-2">
                            <span className="font-bold text-sm">{bot.name}</span>
                            <span className="text-[10px] text-success font-black animate-pulse">● LIVE</span>
                          </div>
                          <div className="flex justify-between text-xs text-gray-500">
                            <span>{bot.type}</span>
                            <span className="font-mono">${parseFloat(bot.trigger_price).toLocaleString()}</span>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-gray-500 italic text-sm border-2 border-dashed border-border/50 rounded-xl">
                        No active strategies found.
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Order Book & History */}
            <div className="col-span-12 lg:col-span-3 space-y-6">
              
              {/* Order Book */}
              <div className="h-[450px]">
                <OrderBook currentPrice={currentPrice} />
              </div>
              
              {/* Recent Trades */}
              <div className="panel flex-1 flex flex-col max-h-[500px]">
                <h3 className="font-bold mb-4 flex items-center gap-2">
                  <History size={18} className="text-primary" /> Market Trades
                </h3>
                <div className="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
                  {trades.length > 0 ? (
                    trades.map((trade, i) => (
                      <div key={i} className="p-3 bg-background/40 rounded-xl border border-border hover:bg-white/5 transition-all flex flex-col gap-2">
                        <div className="flex justify-between items-center">
                          <span className={`text-[10px] font-black px-2 py-0.5 rounded ${trade.type === 'buy' ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                            {trade.type.toUpperCase()}
                          </span>
                          <span className="text-[10px] font-bold text-gray-500 font-mono">
                            {new Date(trade.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                          </span>
                        </div>
                        <div className="flex justify-between items-end">
                          <div className="text-xs font-bold">{trade.amount} <span className="text-gray-500">BTC</span></div>
                          <div className="text-xs font-mono font-bold">${trade.price.toLocaleString()}</div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="py-10 text-center text-gray-500 text-xs italic">
                      Waiting for market activity...
                    </div>
                  )}
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
