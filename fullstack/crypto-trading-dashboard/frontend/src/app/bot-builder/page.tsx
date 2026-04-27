"use client";

import Sidebar from "@/components/Sidebar";
import { Settings, Plus, Play, Trash2, Shield, Zap, Target, Cpu } from "lucide-react";
import { useEffect, useState } from "react";

export default function BotBuilderPage() {
  const [bots, setBots] = useState<any[]>([]);
  const [newBot, setNewBot] = useState({
    name: "Alpha-1 Bot",
    symbol: "BTC",
    type: "price_trigger",
    trigger_price: "80000",
    action: "buy",
    amount: "0.01"
  });

  const fetchBots = async () => {
    try {
      const res = await fetch("http://localhost:8001/api/bots");
      if (res.ok) setBots(await res.json());
    } catch (err) {
      console.error("Failed to fetch bots:", err);
    }
  };

  useEffect(() => {
    fetchBots();
  }, []);

  const handleCreateBot = async () => {
    const updatedBots = [...bots, { ...newBot, id: Date.now(), status: "active" }];
    try {
      const res = await fetch("http://localhost:8001/api/bots", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedBots)
      });
      if (res.ok) {
        fetchBots();
      }
    } catch (err) {
      console.error("Failed to save bot:", err);
    }
  };

  const handleDeleteBot = async (id: number) => {
    const updatedBots = bots.filter(b => b.id !== id);
    try {
      const res = await fetch("http://localhost:8001/api/bots", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedBots)
      });
      if (res.ok) fetchBots();
    } catch (err) {
      console.error("Failed to delete bot:", err);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        <header className="h-20 border-b border-border bg-panel/20 backdrop-blur-md flex items-center px-8 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <Cpu size={24} />
            </div>
            <h2 className="text-xl font-bold tracking-tight">Algorithmic Bot Builder</h2>
          </div>
        </header>

        <div className="p-8 overflow-y-auto flex-1 custom-scrollbar">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 max-w-[1400px] mx-auto">
            
            {/* Create Bot Form */}
            <div className="lg:col-span-4 space-y-6">
              <div className="panel bg-panel/40">
                <h3 className="font-bold mb-8 flex items-center gap-2 text-primary text-lg">
                  <Plus size={20} /> Configure New Strategy
                </h3>
                <div className="space-y-5">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Strategy Name</label>
                    <input 
                      type="text" 
                      value={newBot.name}
                      onChange={(e) => setNewBot({...newBot, name: e.target.value})}
                      className="w-full bg-background/50 border border-border rounded-xl px-4 py-3 focus:outline-none focus:border-primary transition-all font-medium"
                      placeholder="e.g. BTC Moon Bot"
                    />
                  </div>
                  
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Execution Logic</label>
                    <select 
                      className="w-full bg-background/50 border border-border rounded-xl px-4 py-3 focus:outline-none focus:border-primary transition-all font-medium appearance-none"
                      value={newBot.type}
                      onChange={(e) => setNewBot({...newBot, type: e.target.value})}
                    >
                      <option value="price_trigger">Price Trigger</option>
                      <option value="rsi_crossover" disabled>RSI Crossover (Soon)</option>
                      <option value="grid_trading" disabled>Grid Trading (Soon)</option>
                    </select>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Target Price</label>
                      <div className="relative">
                        <input 
                          type="number" 
                          value={newBot.trigger_price}
                          onChange={(e) => setNewBot({...newBot, trigger_price: e.target.value})}
                          className="w-full bg-background/50 border border-border rounded-xl pl-8 pr-4 py-3 focus:outline-none focus:border-primary transition-all font-mono"
                        />
                        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Action</label>
                      <select 
                        className={`w-full bg-background/50 border border-border rounded-xl px-4 py-3 focus:outline-none transition-all font-bold ${
                          newBot.action === 'buy' ? 'text-success border-success/30' : 'text-danger border-danger/30'
                        }`}
                        value={newBot.action}
                        onChange={(e) => setNewBot({...newBot, action: e.target.value})}
                      >
                        <option value="buy">BUY</option>
                        <option value="sell">SELL</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Investment (BTC)</label>
                    <input 
                      type="number" 
                      value={newBot.amount}
                      onChange={(e) => setNewBot({...newBot, amount: e.target.value})}
                      className="w-full bg-background/50 border border-border rounded-xl px-4 py-3 focus:outline-none focus:border-primary transition-all font-mono"
                    />
                  </div>

                  <button 
                    onClick={handleCreateBot}
                    className="w-full btn-primary flex items-center justify-center gap-2 py-4 mt-6 text-base"
                  >
                    <Zap size={20} fill="currentColor" /> Deploy Strategy
                  </button>
                </div>
              </div>
              
              <div className="panel bg-primary/5 border-primary/20 backdrop-blur-md">
                <div className="flex items-center gap-3 text-primary font-black mb-3">
                  <Shield size={20} /> <span className="uppercase tracking-widest text-xs">Risk Management</span>
                </div>
                <p className="text-sm text-gray-400 leading-relaxed">
                  Our neural-engine simulation ensures that your bots operate in a high-fidelity environment. No real capital is deployed.
                </p>
              </div>
            </div>

            {/* Active Bots List */}
            <div className="lg:col-span-8">
              <div className="panel h-full bg-panel/20">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="font-bold text-lg">Active Fleet <span className="text-gray-500 font-normal ml-2">({bots.length})</span></h3>
                  <div className="flex gap-2">
                    <button className="p-2 bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"><History size={18} /></button>
                    <button className="p-2 bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"><Settings size={18} /></button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {bots.map((bot) => (
                    <div key={bot.id} className="bg-background/40 border border-border p-6 rounded-2xl relative group hover:border-primary/40 transition-all overflow-hidden">
                      {/* Decorative gradient */}
                      <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-primary/10 transition-all" />
                      
                      <div className="flex justify-between items-start mb-6 relative z-10">
                        <div>
                          <div className="font-black text-lg tracking-tight mb-1">{bot.name}</div>
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-black bg-white/5 px-2 py-0.5 rounded text-gray-400 uppercase tracking-widest">{bot.type.replace('_', ' ')}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-1.5 bg-success/10 text-success text-[10px] font-black px-2 py-1 rounded-full border border-success/20">
                          <div className="w-1.5 h-1.5 bg-success rounded-full animate-pulse" />
                          RUNNING
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-6 mb-8 relative z-10">
                        <div className="space-y-1">
                          <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Symbol</div>
                          <div className="font-bold flex items-center gap-1.5">
                            <div className="w-5 h-5 rounded-full bg-orange-500/20 flex items-center justify-center text-[10px] text-orange-500">₿</div>
                            {bot.symbol}
                          </div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Trigger</div>
                          <div className="font-mono font-bold text-sm">
                            {bot.action === 'buy' ? '≤' : '≥'} ${parseFloat(bot.trigger_price).toLocaleString()}
                          </div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Allocation</div>
                          <div className="font-bold text-sm">{bot.amount} BTC</div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Performance</div>
                          <div className="font-bold text-sm text-success">+0.00%</div>
                        </div>
                      </div>

                      <button 
                        onClick={() => handleDeleteBot(bot.id)}
                        className="w-full bg-danger/5 hover:bg-danger text-danger hover:text-white border border-danger/20 py-3 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all relative z-10"
                      >
                        <Trash2 size={14} /> Terminate Strategy
                      </button>
                    </div>
                  ))}
                  
                  {bots.length === 0 && (
                    <div className="col-span-full py-24 flex flex-col items-center justify-center text-gray-500 border-2 border-dashed border-border/50 rounded-2xl bg-white/[0.02]">
                      <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
                        <Target size={32} className="text-gray-600" />
                      </div>
                      <p className="font-medium">No active trading bots in your fleet.</p>
                      <p className="text-xs mt-1">Configure and launch a strategy from the left panel.</p>
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
