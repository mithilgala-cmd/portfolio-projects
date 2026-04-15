import React, { useState, useEffect } from 'react';
import { Search, Globe, AlertCircle } from 'lucide-react';
import NewsCard from './components/NewsCard';
import Loader from './components/Loader';
import './index.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');

  // Debounce search
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(searchQuery);
    }, 500);
    return () => clearTimeout(handler);
  }, [searchQuery]);

  useEffect(() => {
    fetchNews();
  }, [debouncedQuery]);

  const fetchNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const endpoint = debouncedQuery 
        ? `http://localhost:8000/news/search?q=${encodeURIComponent(debouncedQuery)}`
        : `http://localhost:8000/news/top-headlines?country=us`;
      
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error('Failed to fetch news');
      }
      
      const data = await response.json();
      setArticles(data.articles || []);
    } catch (err) {
      setError(err.message || 'Something went wrong fetching the news.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo-container">
          <Globe size={32} className="logo-icon" />
          <h1 className="logo-text">Nexus News</h1>
        </div>
        
        <div className="search-container">
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search stories, topics, keywords..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Search size={18} className="search-icon" />
        </div>
      </header>

      <main>
        <div className="section-header">
          <h2 className="section-title">
            {debouncedQuery ? `Results for "${debouncedQuery}"` : 'Top Headlines'}
          </h2>
        </div>

        {loading && <Loader />}
        
        {!loading && error && (
          <div className="status-message">
            <AlertCircle size={48} className="status-icon" />
            <h3>Oops, unable to load news.</h3>
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && articles.length === 0 && (
          <div className="status-message">
            <Search size={48} className="status-icon" color="var(--text-muted)" />
            <h3>No stories found</h3>
            <p>We couldn't find any articles matching your search. Try different keywords.</p>
          </div>
        )}

        {!loading && !error && articles.length > 0 && (
          <div className="news-grid">
            {articles.map((article, index) => (
              <NewsCard key={`${article.url}-${index}`} article={article} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
