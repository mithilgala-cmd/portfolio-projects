import { ResponsiveContainer, AreaChart, Area, Tooltip } from 'recharts';
import { Activity } from 'lucide-react';
import './ActivityChart.css';

export default function ActivityChart({ delay = 0, transactions = [] }) {
  
  // Format the real transaction data into plot points
  // We reverse the sliced array so recent transactions are plotted rightward
  const data = transactions.slice(0, 10).reverse().map((tx, i) => ({
    name: tx.title,
    amt: Math.abs(tx.amount)
  }));
  
  // Fallback data if completely empty
  const chartData = data.length > 0 ? data : [
    { name: 'Empty', amt: 0 }
  ];

  return (
    <div className="activity-chart glass animate-in flex-col" style={{ animationDelay: `${delay}s` }}>
      <div className="chart-header flex-between">
        <div>
          <h3 className="chart-title">Activity Overview</h3>
          <p className="chart-subtitle">Real-time dynamic visualization</p>
        </div>
        <div className="chart-icon flex-center">
          <Activity size={20} />
        </div>
      </div>
      
      <div className="chart-body" style={{ flexGrow: 1, width: '100%', minHeight: '160px', marginTop: '16px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorAmt" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.5}/>
                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <Tooltip 
              contentStyle={{ background: 'var(--bg-base)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-primary)' }}
              itemStyle={{ color: '#0ea5e9', fontWeight: 'bold' }}
              labelStyle={{ color: 'var(--text-secondary)' }}
              formatter={(value) => [`₹${value}`, 'Amount']}
            />
            <Area 
              type="monotone" 
              dataKey="amt" 
              stroke="#0ea5e9" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#colorAmt)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
