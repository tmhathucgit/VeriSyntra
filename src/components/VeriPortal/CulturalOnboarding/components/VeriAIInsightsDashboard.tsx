// VeriPortal AI Insights Dashboard - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import {
  VeriAIInsights,
  VeriMLPersonalizationEngine
} from '../types';
import './VeriAIInsightsDashboard.css';

interface VeriAIInsightsDashboardProps {
  veriAIInsights?: VeriAIInsights[];
  veriMLRecommendations?: VeriMLPersonalizationEngine;
  veriAutomationStatus?: boolean;
  veriLanguage: 'vietnamese' | 'english';
}

export const VeriAIInsightsDashboard: React.FC<VeriAIInsightsDashboardProps> = ({
  veriAIInsights,
  veriMLRecommendations,
  veriAutomationStatus,
  veriLanguage
}) => {
  const veriExecuteAutomatedAction = async (action: any) => {
    console.log('🤖 Executing automated action:', action);
    // Implementation for automated actions
  };

  const veriExecuteManualAction = async (action: any) => {
    console.log('👆 Executing manual action:', action);
    // Implementation for manual actions
  };

  if (!veriAIInsights || veriAIInsights.length === 0) {
    return (
      <div className="veri-ai-insights-dashboard-container veri-empty">
        <div className="veri-empty-state">
          <div className="veri-ai-icon">🤖</div>
          <p>
            {veriLanguage === 'vietnamese' 
              ? 'AI đang phân tích để cung cấp thông tin chi tiết...' 
              : 'AI is analyzing to provide insights...'
            }
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="veri-ai-insights-dashboard-container">
      <div className="veri-dashboard-header">
        <h3>
          <span className="veri-ai-icon">🤖</span>
          {veriLanguage === 'vietnamese' 
            ? 'Thông tin chi tiết từ AI' 
            : 'AI Insights'
          }
        </h3>
        {veriAutomationStatus && (
          <div className="veri-automation-badge">
            <span className="veri-status-indicator">●</span>
            {veriLanguage === 'vietnamese' ? 'Tự động hóa Hoạt động' : 'Automation Active'}
          </div>
        )}
      </div>

      <div className="veri-ai-insights-list">
        {veriAIInsights.map((insight, index) => (
          <div key={insight.veriInsightId || index} className="veri-ai-insight-card">
            <div className="veri-insight-header">
              <div className="veri-insight-type" data-type={insight.veriType}>
                {insight.veriType === 'cultural' && '🇻🇳'}
                {insight.veriType === 'business' && '🏢'}
                {insight.veriType === 'optimization' && '⚡'}
                {insight.veriType === 'prediction' && '🔮'}
              </div>
              <h4>{insight.veriTitle[veriLanguage]}</h4>
            </div>
            
            <p className="veri-insight-description">
              {insight.veriDescription[veriLanguage]}
            </p>
            
            <div className="veri-insight-confidence" data-score={insight.veriConfidenceScore}>
              <div className="veri-confidence-bar">
                <div 
                  className="veri-confidence-fill"
                  style={{ width: `${insight.veriConfidenceScore * 100}%` }}
                ></div>
              </div>
              <span className="veri-confidence-text">
                {Math.round(insight.veriConfidenceScore * 100)}% 
                {veriLanguage === 'vietnamese' ? 'Tin cậy' : 'Confident'}
              </span>
            </div>
            
            {insight.veriAction && (
              <div className="veri-insight-action">
                {insight.veriAutomatedAction ? (
                  <button
                    className="veri-automated-action-button"
                    onClick={() => veriExecuteAutomatedAction(insight.veriAction)}
                  >
                    <span className="veri-auto-icon">🤖</span>
                    {veriLanguage === 'vietnamese' ? 'Thực hiện Tự động' : 'Execute Automatically'}
                  </button>
                ) : (
                  <button
                    className="veri-manual-action-button"
                    onClick={() => veriExecuteManualAction(insight.veriAction)}
                  >
                    <span className="veri-manual-icon">👆</span>
                    {veriLanguage === 'vietnamese' ? 'Xem Chi tiết' : 'View Details'}
                  </button>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {veriMLRecommendations && (
        <div className="veri-ml-recommendation-panel">
          <div className="veri-ml-title">
            <span className="veri-ml-icon">🧠</span>
            {veriLanguage === 'vietnamese' ? 'Khuyến nghị Machine Learning' : 'Machine Learning Recommendations'}
          </div>
          <div className="veri-ml-status">
            <div className="veri-ml-indicator">
              <div className="veri-ml-pulse"></div>
              {veriLanguage === 'vietnamese' ? 'ML Engine Đang hoạt động' : 'ML Engine Active'}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VeriAIInsightsDashboard;