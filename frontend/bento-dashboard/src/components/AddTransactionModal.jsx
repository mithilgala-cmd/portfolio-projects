import { useState } from 'react';
import { X, ArrowDownRight, ArrowUpRight } from 'lucide-react';
import './AddTransactionModal.css';

export default function AddTransactionModal({ isOpen, onClose, onAdd }) {
  const [title, setTitle] = useState('');
  const [amount, setAmount] = useState('');
  const [type, setType] = useState('expense'); // expense, income
  const [category, setCategory] = useState('General');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title || !amount) return;
    onAdd({
      title,
      amount: type === 'expense' ? -Math.abs(Number(amount)) : Math.abs(Number(amount)),
      category,
      type
    });
    setTitle('');
    setAmount('');
    onClose();
  };

  return (
    <div className="modal-overlay flex-center animate-in">
      <div className="modal-content glass">
        <header className="flex-between">
          <h3 style={{ color: 'var(--text-primary)', fontSize: '18px' }}>Add Transaction</h3>
          <button onClick={onClose} className="close-btn"><X size={20} /></button>
        </header>

        <form onSubmit={handleSubmit} className="modal-form flex-col">
          <div className="type-toggle flex-between">
            <button 
              type="button" 
              className={`toggle-btn expense ${type === 'expense' ? 'active' : ''}`}
              onClick={() => setType('expense')}
            >
              <ArrowDownRight size={16} /> Expense
            </button>
            <button 
              type="button" 
              className={`toggle-btn income ${type === 'income' ? 'active' : ''}`}
              onClick={() => setType('income')}
            >
              <ArrowUpRight size={16} /> Income
            </button>
          </div>

          <div className="input-group">
            <label>Title</label>
            <input type="text" placeholder="e.g. Salary, Groceries" value={title} onChange={e => setTitle(e.target.value)} required />
          </div>

          <div className="input-group">
            <label>Amount (₹)</label>
            <input type="number" placeholder="0.00" value={amount} onChange={e => setAmount(e.target.value)} required />
          </div>

          <div className="input-group">
            <label>Category</label>
            <select value={category} onChange={e => setCategory(e.target.value)}>
              <option value="Food">Food & Dining</option>
              <option value="Shopping">Shopping</option>
              <option value="Transport">Transport</option>
              <option value="Income">Income / Salary</option>
              <option value="Equipment">Tech & Equipment</option>
              <option value="Subscription">Subscriptions</option>
              <option value="General">General</option>
            </select>
          </div>

          <button type="submit" className="submit-btn flex-center">Add Record</button>
        </form>
      </div>
    </div>
  );
}
