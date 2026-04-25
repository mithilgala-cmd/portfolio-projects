import { useState } from 'react';
import './TransactionList.css';
import { ArrowDownRight, Coffee, Monitor, Music, Send } from 'lucide-react';

const icons = {
  Monitor: Monitor,
  ArrowDownRight: ArrowDownRight,
  Coffee: Coffee,
  Music: Music,
  Send: Send
};

export default function TransactionList({ delay = 0, transactions = [] }) {
  const [showAll, setShowAll] = useState(false);

  // Format Indian Rupees
  const formatINR = (val) => {
    const isNegative = val < 0;
    const absVal = Math.abs(val);
    const formatted = new Intl.NumberFormat('en-IN', {
      style: 'currency', currency: 'INR', minimumFractionDigits: 0
    }).format(absVal);
    
    return isNegative ? `-${formatted}` : `+${formatted}`;
  };

  const visibleTransactions = showAll ? transactions : transactions.slice(0, 4);

  return (
    <div className="transaction-list glass animate-in" style={{ animationDelay: `${delay}s` }}>
      <div className="list-header flex-between">
        <h3 className="list-title">Recent Transactions</h3>
        <button className="view-all-btn" onClick={() => setShowAll(!showAll)}>
          {showAll ? 'Show Less' : 'View All'}
        </button>
      </div>
      
      <div className="list-items flex-col" style={{ overflowY: 'auto', overflowX: 'hidden', paddingRight: '4px', maxHeight: showAll ? '350px' : 'none' }}>
        {visibleTransactions.map((tx, i) => {
           const IconComp = icons[tx.iconName] || Coffee;
           return (
             <div 
               className="tx-item flex-between animate-in" 
               key={tx.id} 
               style={{ animationDelay: `${delay + 0.1 + (i * 0.05)}s` }}
             >
                <div className="tx-left flex-center">
                   <div 
                     className="tx-icon flex-center" 
                     style={{ backgroundColor: `${tx.color}15`, color: tx.color }}
                   >
                     <IconComp size={18} />
                   </div>
                   <div className="tx-details">
                     <h4 style={{ whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden', maxWidth: '100px' }}>{tx.title}</h4>
                     <span>{tx.category}</span>
                   </div>
                </div>
                <div className={`tx-amount ${tx.type}`}>
                  {formatINR(tx.amount)}
                </div>
             </div>
           );
        })}
      </div>
    </div>
  );
}
