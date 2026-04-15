import { useState, useCallback } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import { Bot, Play, Trash2, Code2, AlertCircle, RotateCcw } from 'lucide-react';
import LanguageSelector, { LANGUAGES } from './components/LanguageSelector';
import ReviewPanel from './components/ReviewPanel';
import Loader from './components/Loader';
import './index.css';

const API_URL = 'http://localhost:8001';

const SAMPLE_CODE = {
  python: `def find_user(users, user_id):
    for i in range(len(users)):
        if users[i]["id"] == user_id:
            return users[i]
    return None

def calculate_stats(data):
    total = 0
    count = 0
    for item in data:
        total = total + int(item["value"])
        count += 1
    avg = total / count
    
    password = "admin123"  # hardcoded credentials
    
    return {"total": total, "average": avg, "count": count}

users = []
result = calculate_stats(users)  # potential ZeroDivisionError
print(result)`,

  javascript: `function getUserData(userId) {
  var data = null;
  
  fetch('http://api.example.com/users/' + userId)
    .then(function(response) {
      data = response.json();
    });
  
  return data; // will always be null
}

function renderUserList(users) {
  var html = '';
  for (var i = 0; i <= users.length; i++) {  // off-by-one error
    html += '<div>' + users[i].name + '</div>';
  }
  document.getElementById('list').innerHTML = html; // XSS vulnerability
  return html;
}`,
};

export default function App() {
  const [language, setLanguage]   = useState('python');
  const [code, setCode]           = useState(SAMPLE_CODE['python']);
  const [status, setStatus]       = useState('idle'); // idle | loading | result | error
  const [result, setResult]       = useState(null);
  const [errorMsg, setErrorMsg]   = useState('');

  const monacoLang = LANGUAGES.find(l => l.value === language)?.monaco || language;

  const handleLanguageChange = useCallback((lang) => {
    setLanguage(lang);
    if (SAMPLE_CODE[lang]) {
      setCode(SAMPLE_CODE[lang]);
      setStatus('idle');
      setResult(null);
    }
  }, []);

  const handleReview = async () => {
    if (!code.trim()) return;
    setStatus('loading');
    setResult(null);
    setErrorMsg('');

    try {
      const { data } = await axios.post(`${API_URL}/review`, {
        code: code.trim(),
        language,
      });
      setResult(data);
      setStatus('result');
    } catch (err) {
      const msg = err?.response?.data?.detail || err.message || 'Unknown error';
      setErrorMsg(msg);
      setStatus('error');
    }
  };

  const handleClear = () => {
    setCode('');
    setStatus('idle');
    setResult(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-brand">
          <div className="brand-icon">
            <Bot size={20} color="#fff" />
          </div>
          <span className="brand-name">CodeReview AI</span>
          <span className="brand-badge">Beta</span>
        </div>
        <span className="header-tagline">Powered by Google Gemini</span>
      </header>

      {/* Main workspace */}
      <div className="workspace">
        {/* Left — Editor */}
        <div className="panel panel-left">
          <div className="panel-header">
            <span className="panel-title">
              <span className="panel-title-dot" />
              <Code2 size={13} />
              Code Editor
            </span>
            <LanguageSelector value={language} onChange={handleLanguageChange} />
          </div>

          <div className="editor-wrap">
            <Editor
              height="100%"
              language={monacoLang}
              value={code}
              onChange={(val) => setCode(val || '')}
              theme="vs-dark"
              options={{
                fontSize: 13,
                fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                fontLigatures: true,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                renderLineHighlight: 'all',
                automaticLayout: true,
                padding: { top: 16, bottom: 16 },
                wordWrap: 'on',
                smoothScrolling: true,
                cursorBlinking: 'smooth',
              }}
            />
          </div>

          <div className="action-bar">
            <button className="btn-clear" onClick={handleClear} title="Clear code">
              <Trash2 size={14} />
              Clear
            </button>
            <span className="char-count">{code.length.toLocaleString()} chars</span>
            <button
              className="btn-review"
              onClick={handleReview}
              disabled={!code.trim() || status === 'loading'}
            >
              <Play size={14} />
              Review Code
            </button>
          </div>
        </div>

        {/* Right — Results */}
        <div className="panel panel-right">
          {status === 'idle' && (
            <div className="review-placeholder">
              <div className="placeholder-icon">
                <Bot size={36} color="var(--accent-light)" />
              </div>
              <p className="placeholder-title">Ready to review your code</p>
              <p className="placeholder-sub">
                Paste any code snippet to get instant AI feedback on quality, security, and performance.
              </p>
              <div className="placeholder-steps">
                {['Write or paste your code', 'Choose the language', 'Click "Review Code"'].map((s, i) => (
                  <div key={i} className="placeholder-step">
                    <span className="step-num">{i + 1}</span>
                    {s}
                  </div>
                ))}
              </div>
            </div>
          )}

          {status === 'loading' && <Loader />}

          {status === 'result' && result && <ReviewPanel result={result} />}

          {status === 'error' && (
            <div className="review-error">
              <div className="error-icon">
                <AlertCircle size={28} />
              </div>
              <p className="error-title">Review Failed</p>
              <p className="error-msg">{errorMsg}</p>
              <button className="btn-retry" onClick={handleReview}>
                <RotateCcw size={13} style={{ marginRight: 6, display: 'inline' }} />
                Retry
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
