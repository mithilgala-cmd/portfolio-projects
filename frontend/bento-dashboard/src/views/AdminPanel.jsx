import { ShieldAlert, Users, Server, Database } from 'lucide-react';
import StatCard from '../components/StatCard';

export default function AdminPanel() {
  return (
    <>
      <header className="flex-between animate-in" style={{ animationDelay: '0.1s', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: '#10b981', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <ShieldAlert size={28} /> Admin Console
          </h1>
          <p>System overview and user management.</p>
        </div>
      </header>
      
      <section className="bento-grid">
         <StatCard title="Registered Users" value="1,24,500" trend={12.5} trendUp={true} icon={Users} delay={0.2} />
         <StatCard title="Server Uptime" value="99.9%" trend={0.1} trendUp={true} icon={Server} delay={0.3} />
         <StatCard title="Database Load" value="42%" trend={4.5} trendUp={false} icon={Database} delay={0.4} />

         <div className="glass animate-in flex-col" style={{ gridColumn: 'span 4', padding: '24px', gap: '16px', animationDelay: '0.5s', minHeight: '300px' }}>
           <h3 style={{ fontSize: '18px', color: 'var(--text-primary)' }}>Recent User Registrations</h3>
           
           <div className="flex-between" style={{ padding: '16px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <span style={{ width: 32, height: 32, borderRadius: '50%', background: '#8b5cf6', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold' }}>A</span>
               <div className="flex-col">
                  <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>Arjun</span>
                  <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>arjun@example.com</span>
               </div>
             </div>
             <span style={{ color: 'var(--text-secondary)', fontSize: 13 }}>2 mins ago</span>
           </div>

           <div className="flex-between" style={{ padding: '16px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px' }}>
             <div className="flex-center" style={{ gap: '12px' }}>
               <span style={{ width: 32, height: 32, borderRadius: '50%', background: '#0ea5e9', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold' }}>P</span>
               <div className="flex-col">
                  <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>Priya Sharma</span>
                  <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>priya@example.com</span>
               </div>
             </div>
             <span style={{ color: 'var(--text-secondary)', fontSize: 13 }}>1 hr ago</span>
           </div>
           
         </div>
      </section>
    </>
  );
}
