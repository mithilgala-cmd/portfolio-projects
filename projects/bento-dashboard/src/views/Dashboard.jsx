import { ArrowUpRight, ArrowDownRight, IndianRupee, Users } from 'lucide-react';
import StatCard from '../components/StatCard';
import ActivityChart from '../components/ActivityChart';
import TransactionList from '../components/TransactionList';
import QuickTransfer from '../components/QuickTransfer';

const formatINR = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

export default function Dashboard({ balance, expenses, transactions, handleTransfer, user }) {
  return (
    <>
      <header className="flex-between animate-in" style={{ animationDelay: '0.1s', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)', marginBottom: '8px' }}>
            Welcome back, {user?.name || 'Arjun'} 👋
          </h1>
          <p>Here's what's happening with your accounts today.</p>
        </div>
        <div 
          className="profile-placeholder glass"
          style={{ 
            width: '48px', 
            height: '48px', 
            borderRadius: '50%', 
            background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
            boxShadow: '0 0 20px rgba(139, 92, 246, 0.4)'
          }}
        ></div>
      </header>

      <section className="bento-grid">
        <StatCard title="Total Balance" value={formatINR(balance)} trend={14.5} trendUp={true} icon={IndianRupee} delay={0.2} />
        <StatCard title="Net Income" value={formatINR(82500)} trend={4.2} trendUp={true} icon={ArrowUpRight} delay={0.3} />
        <StatCard title="Total Expenses" value={formatINR(expenses)} trend={2.1} trendUp={false} icon={ArrowDownRight} delay={0.4} />
        <StatCard title="Active Users" value="14,204" trend={22.4} trendUp={true} icon={Users} delay={0.5} />

        <div style={{ gridColumn: 'span 2' }}>
          <ActivityChart delay={0.6} transactions={transactions} />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <QuickTransfer delay={0.65} onTransfer={handleTransfer} />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <TransactionList delay={0.7} transactions={transactions} />
        </div>
      </section>
    </>
  );
}
