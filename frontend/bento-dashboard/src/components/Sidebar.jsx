import { Home, PieChart, Wallet, Settings, LogOut, ShieldAlert, Sun, Moon } from 'lucide-react';
import './Sidebar.css';

export default function Sidebar({ currentView, onNavigate, onLogout, onOpenModal, user, theme, onToggleTheme }) {
  const navItems = [
    { id: 'dashboard', icon: Home, label: 'Dashboard' },
    { id: 'analytics', icon: PieChart, label: 'Analytics' },
    { id: 'wallet', icon: Wallet, label: 'Wallet' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ];

  // RBAC Inject
  if (user?.role === 'admin') {
    navItems.push({ id: 'admin', icon: ShieldAlert, label: 'Admin Console' });
  }

  return (
    <aside className="sidebar glass flex-col animate-in" style={{ animationDelay: '0.1s' }}>
      <div className="logo flex-center" style={{ padding: '0 8px' }}>
        <div className="logo-icon"></div>
        <h2>Bento.</h2>
      </div>
      
      <nav className="nav-links flex-col">
        {navItems.map(item => (
          <a 
            key={item.id}
            href={`#${item.id}`}
            className={`nav-item ${currentView === item.id ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              onNavigate(item.id);
            }}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </a>
        ))}

        <button 
          onClick={onOpenModal} 
          style={{ 
            marginTop: '16px', padding: '12px', background: 'var(--accent-primary)',
            color: 'white', border: 'none', borderRadius: '12px', cursor: 'pointer',
            fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
            transition: 'transform 0.2s', boxShadow: '0 4px 12px rgba(139, 92, 246, 0.25)'
          }}
          onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
          onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
        >
          <span>+ Add Record</span>
        </button>
      </nav>

      <div className="sidebar-footer flex-col" style={{ gap: '8px' }}>
        <button 
           className="nav-item" 
           onClick={onToggleTheme}
           style={{ background: 'transparent', border: 'none', width: '100%', cursor: 'pointer', outline: 'none' }}
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
        </button>

        <a 
          href="#logout" 
          className="nav-item logout" 
          onClick={(e) => {
            e.preventDefault();
            onLogout();
          }}
        >
          <LogOut size={20} />
          <span>Logout</span>
        </a>
      </div>
    </aside>
  );
}
