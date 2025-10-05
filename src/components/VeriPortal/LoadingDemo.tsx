// VeriPortal Loading Indicator Demo
// This component demonstrates the professional Vietnamese cultural loading indicator

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import '../VeriPortalTheme.css';

const VeriPortalLoadingDemo: React.FC = () => {
  const { t } = useTranslation();
  const [isLoading, setIsLoading] = useState(true);

  // Simulate loading for demo purposes
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 5000); // 5 seconds demo

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="veri-loading-container">
        <div className="veri-loading-content">
          {/* Vietnamese Lotus Logo */}
          <div className="veri-lotus-container">
            <div className="veri-lotus-spinner">
              <div className="veri-lotus-petal veri-petal-1"></div>
              <div className="veri-lotus-petal veri-petal-2"></div>
              <div className="veri-lotus-petal veri-petal-3"></div>
              <div className="veri-lotus-petal veri-petal-4"></div>
              <div className="veri-lotus-petal veri-petal-5"></div>
              <div className="veri-lotus-petal veri-petal-6"></div>
              <div className="veri-lotus-center"></div>
            </div>
          </div>
          
          {/* Vietnamese Flag Accent */}
          <div className="veri-cultural-accent">
            <span className="veri-flag-star">⭐</span>
            <div className="veri-flag-colors">
              <div className="veri-red-stripe"></div>
              <div className="veri-gold-stripe"></div>
            </div>
          </div>

          {/* Loading Text */}
          <div className="veri-loading-text">
            <h3 className="veri-loading-title">
              {t('common:loadingVeriPortal')}
            </h3>
            <p className="veri-loading-subtitle">
              {t('common:loadingDescription')}
            </p>
          </div>

          {/* Progress Bar with Cultural Design */}
          <div className="veri-loading-progress">
            <div className="veri-progress-track">
              <div className="veri-progress-fill"></div>
              <div className="veri-progress-glow"></div>
            </div>
            <div className="veri-loading-dots">
              <span className="veri-dot veri-dot-1"></span>
              <span className="veri-dot veri-dot-2"></span>
              <span className="veri-dot veri-dot-3"></span>
            </div>
          </div>

          {/* Vietnamese Cultural Pattern */}
          <div className="veri-cultural-pattern">
            <div className="veri-pattern-element"></div>
            <div className="veri-pattern-element"></div>
            <div className="veri-pattern-element"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 text-center">
      <h2 className="text-2xl font-bold text-green-600 mb-4">
        🎉 VeriPortal Loading Complete!
      </h2>
      <p className="text-gray-600">
        The professional Vietnamese cultural loading indicator has finished.
        <br />
        Refresh the page to see it again.
      </p>
      <button 
        onClick={() => setIsLoading(true)}
        className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
      >
        Show Loading Again
      </button>
    </div>
  );
};

export default VeriPortalLoadingDemo;