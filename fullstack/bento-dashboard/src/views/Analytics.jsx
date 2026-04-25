import { Activity, BarChart2, TrendingUp } from 'lucide-react';
import ActivityChart from '../components/ActivityChart';
import StatCard from '../components/StatCard';

export default function Analytics({ transactions = [] }) {
  return (
    <>
      <header className="flex-between animate-in" style={{ animationDelay: '0.1s', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)', marginBottom: '8px' }}>Analytics & Reports 📈</h1>
          <p>Deep dive into your financial performance.</p>
        </div>
      </header>
      <section className="bento-grid">
         <StatCard title="Monthly Growth" value="+24.5%" trend={12} trendUp={true} icon={TrendingUp} delay={0.2} />
         <StatCard title="Avg. Transaction" value="₹1,240" trend={5.2} trendUp={true} icon={Activity} delay={0.3} />
         <StatCard title="Conversion Rate" value="3.8%" trend={1.1} trendUp={false} icon={BarChart2} delay={0.4} />
         <div style={{ gridColumn: 'span 4' }}>
            <ActivityChart delay={0.5} transactions={transactions} />
         </div>
      </section>
    </>
  );
}
