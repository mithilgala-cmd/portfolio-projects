"use client";

import { useCallback, useEffect, useState } from "react";

interface OrderBookItem {
  price: number;
  amount: number;
  total: number;
}

export default function OrderBook({ currentPrice }: { currentPrice: number | null }) {
  const [asks, setAsks] = useState<OrderBookItem[]>([]);
  const [bids, setBids] = useState<OrderBookItem[]>([]);

  const fetchDepth = useCallback(async () => {
    try {
      const res = await fetch("http://localhost:8001/api/market-depth");
      if (res.ok) {
        const data = await res.json();
        setAsks(data.asks);
        setBids(data.bids);
      }
    } catch (err) {
      console.error("Failed to fetch market depth:", err);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchDepth();
    }, 0);
    const interval = setInterval(fetchDepth, 2000); // 2s interval is enough for order book
    return () => {
      clearTimeout(timer);
      clearInterval(interval);
    };
  }, [fetchDepth]);

  return (
    <div className="panel h-full flex flex-col overflow-hidden bg-panel/30 backdrop-blur-xl">
      <h3 className="font-black mb-4 text-[10px] uppercase tracking-widest text-gray-500">Live Order Book</h3>
      <div className="grid grid-cols-3 text-[9px] uppercase font-black text-gray-600 mb-2 px-2">
        <span>Price (USDT)</span>
        <span className="text-right">Amount (BTC)</span>
        <span className="text-right">Total</span>
      </div>
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Asks (Sell Orders) */}
        <div className="flex flex-col-reverse mb-1">
          {asks.map((order, i) => (
            <div key={`ask-${i}`} className="grid grid-cols-3 text-[11px] py-0.5 px-2 hover:bg-white/5 transition-colors relative group">
              <div 
                className="absolute inset-0 bg-danger/5 origin-right transition-all duration-500" 
                style={{ width: `${(order.total / (asks[0]?.total || 1)) * 100}%`, right: 0, left: 'auto' }} 
              />
              <span className="text-danger font-mono font-bold relative z-10">{order.price.toFixed(2)}</span>
              <span className="text-right font-mono font-medium relative z-10">{order.amount.toFixed(4)}</span>
              <span className="text-right font-mono text-gray-500 text-[10px] relative z-10">{order.total.toFixed(2)}</span>
            </div>
          ))}
        </div>

        {/* Current Price Divider */}
        <div className="py-3 my-1 border-y border-border/50 flex items-center justify-between px-2 bg-white/[0.02]">
          <span className={`text-lg font-black font-mono tracking-tighter ${asks.length > 0 && bids.length > 0 ? 'text-success' : 'text-gray-400'}`}>
            {currentPrice?.toFixed(2) || "---"}
          </span>
          <div className="text-[10px] font-bold text-gray-500 flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-success rounded-full animate-pulse" />
            LIVE
          </div>
        </div>

        {/* Bids (Buy Orders) */}
        <div className="flex flex-col">
          {bids.map((order, i) => (
            <div key={`bid-${i}`} className="grid grid-cols-3 text-[11px] py-0.5 px-2 hover:bg-white/5 transition-colors relative group">
              <div 
                className="absolute inset-0 bg-success/5 origin-right transition-all duration-500" 
                style={{ width: `${(order.total / (bids[bids.length-1]?.total || 1)) * 100}%`, right: 0, left: 'auto' }} 
              />
              <span className="text-success font-mono font-bold relative z-10">{order.price.toFixed(2)}</span>
              <span className="text-right font-mono font-medium relative z-10">{order.amount.toFixed(4)}</span>
              <span className="text-right font-mono text-gray-500 text-[10px] relative z-10">{order.total.toFixed(2)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
