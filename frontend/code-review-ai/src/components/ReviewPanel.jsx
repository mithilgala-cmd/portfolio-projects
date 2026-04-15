import { useState } from 'react';
import {
  CheckCircle, AlertTriangle, XCircle, Info,
  ChevronDown, TrendingUp, Sparkles, ShieldCheck
} from 'lucide-react';

const SEVERITY_CONFIG = {
  error:   { icon: XCircle,        cls: 'error',   badge: 'sev-error',   label: 'Error'   },
  warning: { icon: AlertTriangle,  cls: 'warning', badge: 'sev-warning', label: 'Warning' },
  info:    { icon: Info,           cls: 'info',    badge: 'sev-info',    label: 'Info'    },
};

function getScoreColor(score) {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#f59e0b';
  return '#ef4444';
}

function IssueCard({ issue }) {
  const [expanded, setExpanded] = useState(false);
  const cfg = SEVERITY_CONFIG[issue.severity] || SEVERITY_CONFIG.info;

  return (
    <div
      className={`issue-card ${cfg.cls} ${expanded ? 'expanded' : ''}`}
      onClick={() => setExpanded(!expanded)}
    >
      <div className="issue-header">
        <span className={`severity-badge ${cfg.badge}`}>{cfg.label}</span>
        <span className="category-badge">{issue.category}</span>
        {issue.line && <span className="issue-line">{issue.line}</span>}
        <ChevronDown size={14} className="issue-expand-icon" style={{ marginLeft: 'auto' }} />
      </div>
      <p className="issue-desc">{issue.description}</p>
      {expanded && issue.suggestion && (
        <div className="issue-suggestion">
          💡 <strong>Suggestion:</strong> {issue.suggestion}
        </div>
      )}
    </div>
  );
}

export default function ReviewPanel({ result }) {
  const { summary, overall_score, complexity, issues, improvements, positive_points } = result;
  const scoreColor = getScoreColor(overall_score);
  const scoreDeg = `${(overall_score / 100) * 360}deg`;

  const errors   = issues.filter(i => i.severity === 'error');
  const warnings = issues.filter(i => i.severity === 'warning');
  const infos    = issues.filter(i => i.severity === 'info');

  return (
    <div className="review-results">
      {/* Score header */}
      <div className="score-header">
        <div
          className="score-circle"
          style={{ '--score-color': scoreColor, '--score-deg': scoreDeg }}
        >
          <span className="score-number">{overall_score}</span>
        </div>
        <div className="score-info">
          <p className="score-summary">{summary}</p>
          <div className="score-meta">
            <span className={`score-badge badge-complexity-${complexity.toLowerCase()}`}>
              <TrendingUp size={11} />
              {complexity} Complexity
            </span>
            {issues.length > 0 && (
              <span className="score-badge badge-issues">
                {issues.length} Issue{issues.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Positive points */}
      {positive_points?.length > 0 && (
        <div className="positives-card">
          <div className="card-title card-title-success">
            <CheckCircle size={14} />
            What's done well
          </div>
          {positive_points.map((pt, i) => (
            <div key={i} className="positive-item">
              <div className="positive-dot" />
              {pt}
            </div>
          ))}
        </div>
      )}

      {/* Issues */}
      {issues.length > 0 && (
        <div className="issues-section">
          <div className="section-label">
            <ShieldCheck size={13} />
            Issues Found ({issues.length})
          </div>
          {errors.length   > 0 && errors.map((iss, i)   => <IssueCard key={`e${i}`} issue={iss} />)}
          {warnings.length > 0 && warnings.map((iss, i) => <IssueCard key={`w${i}`} issue={iss} />)}
          {infos.length    > 0 && infos.map((iss, i)    => <IssueCard key={`i${i}`} issue={iss} />)}
        </div>
      )}

      {/* Improvements */}
      {improvements?.length > 0 && (
        <div className="improvements-card">
          <div className="card-title card-title-accent">
            <Sparkles size={14} />
            Suggested Improvements
          </div>
          {improvements.map((imp, i) => (
            <div key={i} className="improvement-item">
              <span className="improvement-num">{i + 1}</span>
              {imp}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
