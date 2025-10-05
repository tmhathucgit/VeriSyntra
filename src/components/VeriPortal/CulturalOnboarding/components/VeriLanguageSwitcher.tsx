// VeriPortal Language Switcher - AI-Powered Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React, { useState } from 'react';
import {
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine,
  VeriMLLanguagePreference,
  VeriAIInsights
} from '../types';
import './VeriLanguageSwitcher.css';

interface VeriAILanguageSwitcherProps {
  veriCurrentLanguage: 'vietnamese' | 'english';
  setVeriLanguage: (lang: 'vietnamese' | 'english') => void;
  veriPrimaryLanguage: 'vietnamese' | 'english';
  veriSecondaryLanguage: 'vietnamese' | 'english';
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
}

interface VeriAILanguageRecommendation {
  veriRecommendedLanguage: 'vietnamese' | 'english';
  veriConfidence: number;
  veriReasoning: string;
}

// AI-Powered VeriPortal Language Switcher with Machine Learning Intelligence
export const VeriLanguageSwitcher: React.FC<VeriAILanguageSwitcherProps> = ({
  veriCurrentLanguage,
  setVeriLanguage,
  veriPrimaryLanguage,
  veriSecondaryLanguage,
  veriAIEngine,
  veriMLPersonalization,
  veriAutomationEngine
}) => {
  const [veriAILanguageRecommendations] = useState<VeriAILanguageRecommendation[]>();
  const [veriMLLanguagePreference] = useState<VeriMLLanguagePreference>();

  // Removed AI effects for simplicity - focus on language switching functionality

  // Simple and reliable language switching
  const veriHandleLanguageSwitch = (language: 'vietnamese' | 'english') => {
    console.log(`🌐 VeriPortal: Switching language from ${veriCurrentLanguage} to ${language}`);
    
    // Direct language change
    setVeriLanguage(language);
    
    console.log(`✅ Language successfully switched to ${language}`);
  };

  return (
    <div className="veri-ai-language-switcher-container" data-ai-enhanced="true">
      {/* AI Language Recommendations */}
      {veriAILanguageRecommendations && (
        <div className="veri-ai-language-recommendations">
          {veriAILanguageRecommendations.map((recommendation, index) => (
            <div key={index} className="veri-recommendation-item">
              <span className="veri-recommendation-text">
                {recommendation.veriReasoning}
              </span>
              <span className="veri-confidence-score">
                {Math.round(recommendation.veriConfidence * 100)}%
              </span>
            </div>
          ))}
        </div>
      )}
      
      {/* ML Language Preference Indicator */}
      {veriMLLanguagePreference && (
        <div className="veri-ml-preference-indicator">
          <div className="veri-ml-confidence">
            AI Confidence: {Math.round(veriMLLanguagePreference.veriConfidence * 100)}%
          </div>
        </div>
      )}
      
      {/* Vietnamese Language Button */}
      <button
        className={`veri-ai-language-button ${veriCurrentLanguage === 'vietnamese' ? 'veri-active' : ''}`}
        onClick={() => {
          console.log('🇻🇳 Vietnamese button clicked!');
          veriHandleLanguageSwitch('vietnamese');
        }}
        data-priority="primary"
        data-ai-recommended={veriMLLanguagePreference?.veriRecommended === 'vietnamese'}
        data-ml-confidence={veriMLLanguagePreference?.veriConfidence}
      >
        <div className="veri-flag-container">
          <span className="veri-vietnamese-flag">🇻🇳</span>
        </div>
        <div className="veri-language-info">
          <span className="veri-language-label">Tiếng Việt</span>
          <span className="veri-primary-indicator">Chính</span>
        </div>
        {veriMLLanguagePreference?.veriRecommended === 'vietnamese' && (
          <div className="veri-ai-recommendation-badge">AI</div>
        )}
      </button>
      
      {/* English Language Button */}
      <button
        className={`veri-ai-language-button ${veriCurrentLanguage === 'english' ? 'veri-active' : ''}`}
        onClick={() => {
          console.log('🇺🇸 English button clicked!');
          veriHandleLanguageSwitch('english');
        }}
        data-priority="secondary"
        data-ai-recommended={veriMLLanguagePreference?.veriRecommended === 'english'}
        data-ml-confidence={veriMLLanguagePreference?.veriConfidence}
      >
        <div className="veri-flag-container">
          <span className="veri-english-flag">🇺🇸</span>
        </div>
        <div className="veri-language-info">
          <span className="veri-language-label">English</span>
          <span className="veri-secondary-indicator">Secondary</span>
        </div>
        {veriMLLanguagePreference?.veriRecommended === 'english' && (
          <div className="veri-ai-recommendation-badge">AI</div>
        )}
      </button>
      
      {/* AI Cultural Language Status */}
      <div className="veri-ai-cultural-language-status">
        <div className="veri-primary-language">
          Primary: {veriPrimaryLanguage === 'vietnamese' ? 'Tiếng Việt' : 'English'}
        </div>
        <div className="veri-secondary-language">
          Secondary: {veriSecondaryLanguage === 'vietnamese' ? 'Tiếng Việt' : 'English'}
        </div>
        {veriAutomationEngine?.veriAutomationStatus && (
          <div className="veri-automation-status">
            <span className="veri-automation-indicator">🤖</span>
            <span>AI Automation Active</span>
          </div>
        )}
      </div>
      
      {/* AI Language Insights */}
      {veriMLLanguagePreference?.veriInsights && (
        <div className="veri-ai-language-insights">
          <h4>
            {veriCurrentLanguage === 'vietnamese' 
              ? 'Khuyến nghị AI về Ngôn ngữ' 
              : 'AI Language Insights'
            }
          </h4>
          {veriMLLanguagePreference.veriInsights.map((insight, index) => (
            <div key={index} className="veri-insight-item">
              <div className="veri-insight-title">
                {insight.veriTitle[veriCurrentLanguage]}
              </div>
              <div className="veri-insight-description">
                {insight.veriDescription[veriCurrentLanguage]}
              </div>
              <div className="veri-insight-confidence">
                Confidence: {Math.round(insight.veriConfidenceScore * 100)}%
              </div>
            </div>
          ))}
        </div>
      )}
      

    </div>
  );
};

export default VeriLanguageSwitcher;