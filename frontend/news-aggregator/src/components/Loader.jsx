import React from 'react';

const Loader = () => {
  return (
    <div className="loader-container">
      <div className="loader">
        <div className="loader-ring"></div>
        <div className="loader-core"></div>
      </div>
      <p className="loader-text">Fetching latest stories...</p>
    </div>
  );
};

export default Loader;
