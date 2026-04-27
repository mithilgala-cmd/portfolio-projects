"use client";

import { useEffect, useRef, useState } from "react";
import { 
  createChart, 
  IChartApi, 
  ISeriesApi, 
  CandlestickData, 
  Time, 
  CandlestickSeries, 
  CrosshairMode,
  LineSeries,
  HistogramSeries
} from "lightweight-charts";

export default function TradingChart({ onPriceUpdate }: { onPriceUpdate?: (price: number) => void }) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<"Histogram"> | null>(null);
  const smaSeriesRef = useRef<ISeriesApi<"Line"> | null>(null);
  
  const [isConnected, setIsConnected] = useState(false);
  const [currentPrice, setCurrentPrice] = useState<number | null>(null);
  const [dataPoints, setDataPoints] = useState<any[]>([]);

  // Function to calculate SMA
  const calculateSMA = (data: any[], period: number) => {
    const sma = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) continue;
      const sum = data.slice(i - period + 1, i + 1).reduce((acc, val) => acc + val.close, 0);
      sma.push({ time: data[i].time, value: sum / period });
    }
    return sma;
  };

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // Initialize chart
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: "transparent" },
        textColor: "#94a3b8",
        fontFamily: "'Inter', sans-serif",
      },
      grid: {
        vertLines: { color: "rgba(51, 65, 85, 0.3)" },
        horzLines: { color: "rgba(51, 65, 85, 0.3)" },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: "rgba(51, 65, 85, 0.5)",
      },
      rightPriceScale: {
        borderColor: "rgba(51, 65, 85, 0.5)",
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: {
          labelBackgroundColor: "#3b82f6",
        },
        horzLine: {
          labelBackgroundColor: "#3b82f6",
        },
      },
      handleScale: {
        axisPressedMouseMove: true,
      },
      autoSize: true,
    });

    const candlestickSeries = chart.addSeries(CandlestickSeries, {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: "#3b82f6",
      priceFormat: {
        type: "volume",
      },
      priceScaleId: "", // overlay
    });

    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    });

    const smaSeries = chart.addSeries(LineSeries, {
      color: "#f59e0b",
      lineWidth: 2,
      priceLineVisible: false,
    });

    chartRef.current = chart;
    candlestickSeriesRef.current = candlestickSeries;
    volumeSeriesRef.current = volumeSeries;
    smaSeriesRef.current = smaSeries;

    // Connect to FastAPI WebSocket
    const ws = new WebSocket("ws://localhost:8001/ws/market");

    ws.onopen = () => {
      setIsConnected(true);
      console.log("Connected to Market Data WS");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data && data.time) {
        const candle: CandlestickData<Time> = {
          time: data.time as Time,
          open: data.open,
          high: data.high,
          low: data.low,
          close: data.close,
        };
        
        candlestickSeries.update(candle);
        
        // Mock volume for visualization
        volumeSeries.update({
          time: data.time as Time,
          value: Math.random() * 100,
          color: data.close >= data.open ? "rgba(16, 185, 129, 0.5)" : "rgba(239, 68, 68, 0.5)",
        });

        setCurrentPrice(data.close);
        if (onPriceUpdate) onPriceUpdate(data.close);

        // Update SMA (Simplified logic: keep track of last N points)
        setDataPoints(prev => {
          const newData = [...prev, candle];
          if (newData.length > 50) newData.shift();
          
          if (newData.length >= 20) {
            const sma = calculateSMA(newData, 20);
            if (sma.length > 0) {
              smaSeries.setData(sma);
            }
          }
          return newData;
        });
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log("Disconnected from Market Data WS");
    };

    // Cleanup
    return () => {
      ws.close();
      chart.remove();
    };
  }, []);

  return (
    <div className="panel h-full flex flex-col min-h-[450px]">
      <div className="flex justify-between items-center mb-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold tracking-tight">BTC/USDT</h2>
            <span className="bg-primary/10 text-primary text-[10px] font-bold px-2 py-0.5 rounded border border-primary/20">
              BINANCE LIVE
            </span>
          </div>
          <div className="flex items-center gap-2 mt-1">
            <span
              className={`w-2 h-2 rounded-full animate-pulse ${
                isConnected ? "bg-success shadow-[0_0_8px_rgba(16,185,129,0.5)]" : "bg-danger"
              }`}
            />
            <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">
              {isConnected ? "Live Market Stream" : "Disconnected"}
            </span>
          </div>
        </div>
        {currentPrice && (
          <div className="text-right">
            <div className="text-3xl font-bold font-mono tracking-tighter text-success">
              ${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
            <div className="text-[10px] text-gray-500 font-mono mt-0.5">
              LAST TRADED PRICE
            </div>
          </div>
        )}
      </div>
      <div ref={chartContainerRef} className="flex-1 w-full" />
    </div>
  );
}
