import React from 'react';
import { ExternalLink, Calendar, User } from 'lucide-react';

const NewsCard = ({ article }) => {
  const { title, description, url, url_to_image, published_at, source, author } = article;
  
  // Format date
  const formattedDate = published_at 
    ? new Date(published_at).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })
    : 'Unknown Date';

  const defaultImage = "https://images.unsplash.com/photo-1546422904-90eab23c3d7e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80";

  return (
    <a href={url} target="_blank" rel="noopener noreferrer" className="news-card">
      <div className="news-card-image-wrapper">
        <img 
          src={url_to_image || defaultImage} 
          alt={title} 
          className="news-card-image" 
          onError={(e) => { e.target.src = defaultImage }}
        />
        <div className="news-card-source">
          {source?.name || 'Unknown Source'}
        </div>
      </div>
      
      <div className="news-card-content">
        <h3 className="news-card-title">{title}</h3>
        <p className="news-card-desc">{description}</p>
        
        <div className="news-card-footer">
          <div className="news-card-meta">
            {author && (
              <span className="meta-item">
                <User size={14} />
                <span className="meta-text">{author.split(',')[0]}</span>
              </span>
            )}
            <span className="meta-item">
              <Calendar size={14} />
              <span className="meta-text">{formattedDate}</span>
            </span>
          </div>
          <div className="news-card-icon">
            <ExternalLink size={18} />
          </div>
        </div>
      </div>
    </a>
  );
};

export default NewsCard;
