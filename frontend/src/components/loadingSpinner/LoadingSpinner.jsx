import React from 'react';
import './loadingSpinner.css';

function LoadingSpinner({ style }) {
  return (
    <div className="spinner" style={style}>
      <div className="double-bounce1"></div>
      <div className="double-bounce2"></div>
    </div>
  );
};

export default LoadingSpinner;