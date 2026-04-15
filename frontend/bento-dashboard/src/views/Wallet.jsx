import QuickTransfer from '../components/QuickTransfer';
import TransactionList from '../components/TransactionList';

export default function Wallet({ balance, transactions, handleTransfer }) {
  return (
    <>
      <header className="flex-between animate-in" style={{ animationDelay: '0.1s', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)', marginBottom: '8px' }}>Your Wallet 💳</h1>
          <p>Manage your funds and execute transfers.</p>
        </div>
      </header>
      <section className="bento-grid" style={{ gridTemplateColumns: 'repeat(2, 1fr)' }}>
        <div style={{ gridColumn: 'span 1', height: '100%' }}>
          <QuickTransfer delay={0.2} onTransfer={handleTransfer} />
        </div>
        <div style={{ gridColumn: 'span 1' }}>
          <TransactionList delay={0.3} transactions={transactions} />
        </div>
      </section>
    </>
  );
}
