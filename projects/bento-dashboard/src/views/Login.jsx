import { useState } from 'react';
import { User, Shield } from 'lucide-react';
import './Login.css';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const submitLogin = (e, role) => {
    e.preventDefault();
    if (!username) return;
    onLogin({ name: username, role });
  };

  return (
    <div className="login-container flex-center animate-in">
      <div className="login-box glass flex-col">
        <div className="login-header flex-col flex-center">
          <div className="logo-icon" style={{ 
            width: 48, height: 48, 
            background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))', 
            borderRadius: '14px', marginBottom: 16,
            boxShadow: '0 8px 16px rgba(139, 92, 246, 0.4)'
          }}></div>
          <h2>Welcome to Bento.</h2>
          <p>Please enter your details to sign in.</p>
        </div>

        <form className="login-form flex-col">
          <div className="input-group">
            <label>Username</label>
            <input 
               type="text" 
               placeholder="Enter your username" 
               value={username} 
               onChange={e => setUsername(e.target.value)} 
               required 
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input 
               type="password" 
               placeholder="••••••••" 
               value={password} 
               onChange={e => setPassword(e.target.value)} 
               required 
            />
          </div>

          <div className="login-actions flex-col" style={{ gap: '12px', marginTop: '12px' }}>
            <button 
              className="submit-btn flex-center" 
              onClick={(e) => submitLogin(e, 'user')}
              style={{ gap: '8px' }}
            >
              <User size={18} /> Login as User
            </button>
            <button 
              className="submit-btn admin flex-center" 
              onClick={(e) => submitLogin(e, 'admin')}
              style={{ 
                background: 'rgba(255,255,255,0.05)', 
                color: 'var(--text-primary)', 
                border: '1px solid var(--border-color)', 
                gap: '8px',
                transition: 'all 0.2s'
              }}
            >
              <Shield size={18} color="var(--accent-success)" /> Login as System Admin
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
