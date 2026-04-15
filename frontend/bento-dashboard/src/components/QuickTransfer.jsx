import { useState } from 'react';
import './QuickTransfer.css';
import { Send, IndianRupee, CheckCircle2, ChevronRight } from 'lucide-react';

export default function QuickTransfer({ delay = 0, onTransfer }) {
  const [amount, setAmount] = useState('');
  const [selectedContact, setSelectedContact] = useState('Priya');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  
  const [isAddingContact, setIsAddingContact] = useState(false);
  const [newContactName, setNewContactName] = useState('');

  const [contacts, setContacts] = useState([
    { name: 'Priya', color: '#8b5cf6' },
    { name: 'Rahul', color: '#0ea5e9' },
    { name: 'Amit', color: '#10b981' },
  ]);

  const handleSend = () => {
    if (!amount || isNaN(amount) || Number(amount) <= 0) {
      setStatus('error');
      setTimeout(() => setStatus('idle'), 2000);
      return;
    }

    setStatus('loading');
    
    setTimeout(() => {
      const success = onTransfer(selectedContact, amount);
      if (success) {
        setStatus('success');
        setAmount('');
        setTimeout(() => setStatus('idle'), 3000);
      } else {
        setStatus('error'); 
        setTimeout(() => setStatus('idle'), 2000);
      }
    }, 800);
  };

  const submitNewContact = (e) => {
    e.preventDefault();
    if (!newContactName.trim()) {
      setIsAddingContact(false);
      return;
    }
    const colors = ['#f59e0b', '#ec4899', '#14b8a6', '#f43f5e'];
    const randomColor = colors[contacts.length % colors.length];
    
    // Keep max 3 contacts visible to preserve the beautiful layout
    let updatedContacts = [...contacts, { name: newContactName.trim(), color: randomColor }];
    if (updatedContacts.length > 3) {
      updatedContacts = updatedContacts.slice(updatedContacts.length - 3);
    }
    
    setContacts(updatedContacts);
    setSelectedContact(newContactName.trim());
    setNewContactName('');
    setIsAddingContact(false);
  };

  return (
    <div className="quick-transfer glass animate-in flex-col" style={{ animationDelay: `${delay}s` }}>
      <h3 className="qt-title">Quick UPI Transfer</h3>
      
      <div className="qt-contacts flex-between" style={{ minHeight: '62px' }}>
        {!isAddingContact ? (
          <>
            {contacts.map((c, i) => (
              <div 
                key={i} 
                className="qt-contact flex-col flex-center"
                onClick={() => setSelectedContact(c.name)}
              >
                <div 
                  className="qt-avatar flex-center" 
                  style={{ 
                    backgroundColor: `${c.color}15`, 
                    color: c.color,
                    border: selectedContact === c.name ? `2px solid ${c.color}` : '2px solid transparent',
                    transform: selectedContact === c.name ? 'scale(1.08)' : 'scale(1)'
                  }}
                >
                  {c.name[0].toUpperCase()}
                </div>
                <span style={{ 
                  color: selectedContact === c.name ? 'var(--text-primary)' : 'var(--text-secondary)',
                  fontWeight: selectedContact === c.name ? 600 : 500
                }}>
                  {c.name.length > 6 ? c.name.substring(0, 5) + '..' : c.name}
                </span>
              </div>
            ))}
            <div 
               className="qt-contact flex-col flex-center"
               onClick={() => setIsAddingContact(true)}
            >
              <div className="qt-avatar flex-center" style={{ backgroundColor: 'rgba(255,255,255,0.05)', border: '2px dashed rgba(255,255,255,0.2)' }}>
                +
              </div>
              <span>New</span>
            </div>
          </>
        ) : (
          <form onSubmit={submitNewContact} className="flex-center animate-in" style={{ width: '100%', gap: '8px', animationDuration: '0.2s' }}>
            <input 
              autoFocus
              type="text" 
              placeholder="UPI ID or Name..." 
              value={newContactName}
              onChange={(e) => setNewContactName(e.target.value.substring(0, 15))}
              style={{ 
                flexGrow: 1, padding: '10px 14px', borderRadius: '12px', 
                border: '1px solid var(--accent-primary)', background: 'rgba(0,0,0,0.3)',
                color: 'white', outline: 'none', fontSize: '13px'
              }}
            />
            <button type="submit" style={{ padding: '8px 12px', borderRadius: '12px', border: 'none', background: 'var(--accent-primary)', color: 'white', cursor: 'pointer' }}>
              <ChevronRight size={18} />
            </button>
          </form>
        )}
      </div>

      <div className={`qt-input-group flex-between ${status === 'error' ? 'error-shake' : ''}`}>
        <div className="qt-currency flex-center">
          <IndianRupee size={16} />
        </div>
        <input 
          type="number" 
          placeholder="0.00" 
          className="qt-input" 
          value={amount}
          onChange={(e) => {
            // Hard limit input length to prevent UI overflow (7 digits = ₹99,99,999)
            if (e.target.value.length <= 7) {
              setAmount(e.target.value);
            }
          }}
          disabled={status === 'loading' || status === 'success'}
        />
      </div>

      <button 
        className={`qt-send-btn flex-center ${status === 'success' ? 'success' : ''}`}
        onClick={handleSend}
        disabled={status === 'loading' || status === 'success'}
        style={{ 
           background: status === 'success' ? '#10b981' : '',
           opacity: (!amount && status !== 'success') ? 0.6 : 1,
           cursor: status === 'loading' ? 'wait' : (!amount ? 'not-allowed' : 'pointer')
        }}
      >
        {status === 'loading' ? (
          <span>Connecting to bank...</span>
        ) : status === 'success' ? (
          <>
            <span>Transfer Successful!</span>
            <CheckCircle2 size={16} />
          </>
        ) : (
          <>
            <span>Send Money</span>
            <Send size={16} />
          </>
        )}
      </button>
    </div>
  );
}
