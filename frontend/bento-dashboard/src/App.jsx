import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './views/Dashboard';
import Analytics from './views/Analytics';
import Wallet from './views/Wallet';
import Settings from './views/Settings';
import AdminPanel from './views/AdminPanel';
import Login from './views/Login';
import AddTransactionModal from './components/AddTransactionModal';

const DEFAULT_TX = [
  { id: 1, title: 'Reliance Digital', category: 'Equipment', amount: -105900, iconName: 'Monitor', type: 'expense', color: '#0ea5e9' },
  { id: 2, title: 'Upwork Payout', category: 'Income', amount: 45000, iconName: 'ArrowDownRight', type: 'income', color: '#10b981' },
  { id: 3, title: 'Zomato', category: 'Food', amount: -450, iconName: 'Coffee', type: 'expense', color: '#f59e0b' },
];

export default function App() {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('bento_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('bento_theme') || 'dark';
  });

  const [currentView, setCurrentView] = useState('dashboard');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [balance, setBalance] = useState(() => {
    const saved = localStorage.getItem('bento_balance');
    return saved ? Number(saved) : 1245000;
  });
  const [expenses, setExpenses] = useState(() => {
    const saved = localStorage.getItem('bento_expenses');
    return saved ? Number(saved) : 106350;
  });
  const [transactions, setTransactions] = useState(() => {
    const saved = localStorage.getItem('bento_transactions');
    return saved ? JSON.parse(saved) : DEFAULT_TX;
  });

  useEffect(() => {
    if (user) localStorage.setItem('bento_user', JSON.stringify(user));
    else localStorage.removeItem('bento_user');
    
    localStorage.setItem('bento_theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    
    // Finance state
    localStorage.setItem('bento_balance', balance.toString());
    localStorage.setItem('bento_expenses', expenses.toString());
    localStorage.setItem('bento_transactions', JSON.stringify(transactions));
  }, [user, theme, balance, expenses, transactions]);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentView('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
  };

  const handleTransfer = (contactName, amount) => {
    const numAmount = Number(amount);
    if (!numAmount || numAmount <= 0 || numAmount > balance) return false;

    setBalance(prev => prev - numAmount);
    setExpenses(prev => prev + numAmount);

    const newTx = {
      id: Date.now(),
      title: `UPI: ${contactName}`,
      category: 'Transfer',
      amount: -numAmount,
      iconName: 'Send',
      type: 'expense',
      color: '#8b5cf6' 
    };

    setTransactions(prev => [newTx, ...prev]);
    return true; 
  };

  const handleAddCustomTransaction = (tx) => {
    const newTx = {
      id: Date.now(),
      title: tx.title,
      category: tx.category,
      amount: tx.amount,
      iconName: tx.type === 'income' ? 'ArrowDownRight' : 'ShoppingBag',
      type: tx.type,
      color: tx.type === 'income' ? '#10b981' : '#f59e0b'
    };
    
    setTransactions(prev => [newTx, ...prev]);
    if (tx.type === 'income') {
      setBalance(b => b + tx.amount);
    } else {
      setBalance(b => b + tx.amount);
      setExpenses(e => e + Math.abs(tx.amount));
    }
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const renderView = () => {
    switch(currentView) {
      case 'dashboard': return <Dashboard balance={balance} expenses={expenses} transactions={transactions} handleTransfer={handleTransfer} user={user} />;
      case 'analytics': return <Analytics transactions={transactions} />;
      case 'wallet': return <Wallet balance={balance} transactions={transactions} handleTransfer={handleTransfer} />;
      case 'settings': return <Settings user={user} theme={theme} onToggleTheme={toggleTheme} />;
      case 'admin': return user.role === 'admin' ? <AdminPanel /> : <Dashboard />;
      default: return <Dashboard balance={balance} expenses={expenses} transactions={transactions} handleTransfer={handleTransfer} user={user} />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar 
        currentView={currentView} 
        onNavigate={setCurrentView} 
        onLogout={handleLogout} 
        onOpenModal={() => setIsModalOpen(true)}
        user={user}
        theme={theme}
        onToggleTheme={toggleTheme}
      />
      <main className="main-content">
        {renderView()}
      </main>

      <AddTransactionModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onAdd={handleAddCustomTransaction} 
      />
    </div>
  );
}
