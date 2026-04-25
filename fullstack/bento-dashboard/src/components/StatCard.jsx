import './StatCard.css';

export default function StatCard({ title, value, trend, trendUp, icon: Icon, delay }) {
  return (
    <div className="stat-card glass animate-in" style={{ animationDelay: `${delay}s` }}>
      <div className="stat-header flex-between">
        <h3 className="stat-title">{title}</h3>
        <div className="stat-icon flex-center">
          <Icon size={20} />
        </div>
      </div>
      
      <div className="stat-body">
        <h2 className="stat-value">{value}</h2>
        <div className={`stat-trend ${trendUp ? 'trend-up' : 'trend-down'}`}>
          <span className="trend-badge">
            {trendUp ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
          <span className="trend-text">vs last month</span>
        </div>
      </div>
    </div>
  );
}
