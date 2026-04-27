"use client";

import Sidebar from "@/components/Sidebar";
import { Wallet, TrendingUp, TrendingDown, Clock, ArrowUpRight, ArrowDownLeft, PieChart, Landmark } from "lucide-react";
import { useEffect, useState } from "react";

export default function PortfolioPage() {
  const [portfolio, setPortfolio] = useState<any>(null);
  const [trades, setTrades] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [portRes, tradesRes] = await Promise.all([
          fetch("http://localhost:8001/api/portfolio"),
          fetch("http://localhost:8001/api/trades")
        ]);
        
        if (portRes.ok) setPortfolio(await portRes.json());
        if (tradesRes.ok) setTrades(await tradesRes.json());
      } catch (err) {
        console.error("Failed to fetch portfolio data:", err);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        <header className="h-20 border-b border-border bg-panel/20 backdrop-blur-md flex items-center px-8 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <Landmark size={24} />
            </div>
            <h2 className="text-xl font-bold tracking-tight">Financial Assets & History</h2>
          </div>
        </header>

        <div className="p-8 overflow-y-auto flex-1 custom-scrollbar">
          <div className="space-y-8 max-w-[1400px] mx-auto">
            
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="panel bg-panel/40 relative overflow-hidden group">
                <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-success/5 rounded-full blur-2xl group-hover:bg-success/10 transition-all" />
                <div className="text-[10px] font-black text-gray-500 mb-2 uppercase tracking-widest flex items-center gap-2">
                  <PieChart size={14} className="text-primary" /> Total Net Worth
                </div>
                <div className="text-4xl font-black font-mono text-success tracking-tighter">
                  ${portfolio?.balance_usd?.toLocaleString(undefined, { minimumFractionDigits: 2 }) || "0.00"}
                </div>
                <div className="mt-2 text-xs text-gray-500 font-medium">Available for immediate deployment</div>
              </div>

              <div className="panel bg-panel/40 relative overflow-hidden group">
                <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-primary/5 rounded-full blur-2xl group-hover:bg-primary/10 transition-all" />
                <div className="text-[10px] font-black text-gray-500 mb-2 uppercase tracking-widest flex items-center gap-2">
                  <div className="w-4 h-4 rounded-full bg-orange-500/20 flex items-center justify-center text-[10px] text-orange-500 font-bold">₿</div> BTC Holdings
                </div>
                <div className="text-4xl font-black font-mono tracking-tighter">
                  {portfolio?.assets?.BTC?.toFixed(4) || "0.0000"} <span className="text-gray-500 text-xl font-bold">BTC</span>
                </div>
                <div className="mt-2 text-xs text-gray-500 font-medium">Value: ~${(portfolio?.assets?.BTC * 80000 || 0).toLocaleString()}</div>
              </div>

              <div className="panel bg-panel/40 relative overflow-hidden group">
                <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-success/5 rounded-full blur-2xl group-hover:bg-success/10 transition-all" />
                <div className="text-[10px] font-black text-gray-500 mb-2 uppercase tracking-widest flex items-center gap-2">
                  <TrendingUp size={14} className="text-success" /> Performance (24h)
                </div>
                <div className="text-4xl font-black font-mono text-success flex items-center gap-2 tracking-tighter">
                  +12.4<span className="text-xl">%</span>
                </div>
                <div className="mt-2 text-xs text-gray-500 font-medium flex items-center gap-1">
                  <ArrowUpRight size={14} /> Outperforming market average
                </div>
              </div>
            </div>

            {/* Trade History Table */}
            <div className="panel bg-panel/20">
              <div className="flex items-center justify-between mb-8">
                <h3 className="font-black text-lg flex items-center gap-2 uppercase tracking-tighter">
                  <Clock size={20} className="text-primary" /> Execution History
                </h3>
                <div className="flex gap-2">
                  <button className="px-4 py-2 bg-white/5 rounded-xl text-xs font-bold text-gray-400 hover:text-white transition-all">Export CSV</button>
                  <button className="px-4 py-2 bg-white/5 rounded-xl text-xs font-bold text-gray-400 hover:text-white transition-all">Filter</button>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="text-[10px] font-black text-gray-500 uppercase tracking-widest border-b border-border/50">
                      <th className="pb-6 font-bold">Timestamp</th>
                      <th className="pb-6 font-bold">Operation</th>
                      <th className="pb-6 font-bold">Asset</th>
                      <th className="pb-6 font-bold text-right">Volume</th>
                      <th className="pb-6 font-bold text-right">Execution Price</th>
                      <th className="pb-6 font-bold text-right">Total (USD)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/30">
                    {trades.map((trade, i) => (
                      <tr key={i} className="text-sm group hover:bg-white/[0.02] transition-all">
                        <td className="py-5 text-gray-400 font-medium">
                          {new Date(trade.timestamp * 1000).toLocaleString()}
                        </td>
                        <td className="py-5">
                          <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black tracking-widest ${
                            trade.type === 'buy' ? 'bg-success/10 text-success border border-success/20' : 'bg-danger/10 text-danger border border-danger/20'
                          }`}>
                            {trade.type === 'buy' ? <ArrowUpRight size={12} /> : <ArrowDownLeft size={12} />}
                            {trade.type.toUpperCase()}
                          </div>
                        </td>
                        <td className="py-5">
                          <div className="flex items-center gap-2 font-black">
                            <div className="w-6 h-6 rounded-full bg-orange-500/10 flex items-center justify-center text-[10px] text-orange-500 border border-orange-500/20">₿</div>
                            {trade.symbol}
                          </div>
                        </td>
                        <td className="py-5 font-mono font-bold text-right text-gray-300">{trade.amount.toFixed(6)}</td>
                        <td className="py-5 font-mono font-bold text-right">${trade.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                        <td className="py-5 font-mono font-black text-right text-white">
                          ${(trade.amount * trade.price).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                        </td>
                      </tr>
                    ))}
                    {trades.length === 0 && (
                      <tr>
                        <td colSpan={6} className="py-24 text-center text-gray-500 italic">
                          <div className="flex flex-col items-center justify-center opacity-50">
                            <History size={48} className="mb-4" />
                            <p className="font-medium">No ledger entries found.</p>
                          </div>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
