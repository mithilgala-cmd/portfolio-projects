import { useState } from 'react';
import { Bell, Lock, User, Shield } from 'lucide-react';

export default function Settings({ user }) {
  const [twoFactor, setTwoFactor] = useState(false);
  const [pushAlerts, setPushAlerts] = useState(true);

  return (
    <>
      <header className="flex-between animate-in" style={{ animationDelay: '0.1s', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)', marginBottom: '8px' }}>Preferences ⚙️</h1>
          <p>Customize your dashboard experience.</p>
        </div>
      </header>
      
      <section className="bento-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
         <div className="glass animate-in flex-col" style={{ padding: '24px', gap: '16px', animationDelay: '0.2s', height: 'fit-content' }}>
           <h3 style={{ fontSize: '18px', color: 'var(--text-primary)' }}>Profile Info</h3>
           
           <div className="flex-between" style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <User size={20} color="var(--accent-secondary)" />
               <span>Display Name</span>
             </div>
             <span style={{ color: 'var(--text-primary)', fontWeight: 'bold' }}>{user?.name || 'Arjun'}</span>
           </div>
           
           <div className="flex-between" style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <Shield size={20} color="var(--accent-success)" />
               <span>Account Status</span>
             </div>
             <span style={{ color: '#10b981', fontWeight: 'bold' }}>{user?.role === 'admin' ? 'Admin Node' : 'Verified'}</span>
           </div>
         </div>

         <div className="glass animate-in flex-col" style={{ padding: '24px', gap: '16px', animationDelay: '0.3s', height: 'fit-content' }}>
           <h3 style={{ fontSize: '18px', color: 'var(--text-primary)' }}>Security & Notifications</h3>
           
           <div className="flex-between" style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <Lock size={20} color={twoFactor ? "var(--accent-success)" : "var(--text-secondary)"} />
               <span>Two-Factor Auth</span>
             </div>
             <button 
               onClick={() => setTwoFactor(!twoFactor)}
               style={{ 
                 padding: '8px 16px', 
                 background: twoFactor ? 'rgba(16, 185, 129, 0.2)' : 'var(--accent-primary)', 
                 color: twoFactor ? '#10b981' : 'white', 
                 border: 'none', 
                 borderRadius: '8px', 
                 cursor: 'pointer', 
                 fontWeight: 600,
                 transition: 'all 0.2s'
               }}
             >
               {twoFactor ? 'Enabled' : 'Enable'}
             </button>
           </div>
           
           <div className="flex-between" style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <Bell size={20} color={pushAlerts ? "var(--accent-success)" : "var(--text-secondary)"} />
               <span>Push Alerts</span>
             </div>
             <button 
               onClick={() => setPushAlerts(!pushAlerts)}
               style={{ 
                 background: 'transparent', border: 'none', color: pushAlerts ? '#10b981' : 'var(--text-muted)',
                 cursor: 'pointer', fontWeight: 600
               }}
             >
               {pushAlerts ? 'Opted In' : 'Opted Out'}
             </button>
           </div>
         </div>
      </section>
    </>
  );
}
