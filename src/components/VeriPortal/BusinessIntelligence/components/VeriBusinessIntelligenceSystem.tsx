// VeriPortal_05_BusinessIntelligence - Main System Component
// Vietnamese Business Intelligence & Analytics Platform

import React, { useState, useEffect } from 'react';
import { useLanguageSwitch } from '../../../../hooks/useCulturalIntelligence';
import { VeriSyntraBanner } from '../../../shared/VeriSyntraBanner';
import {
  VeriBusinessIntelligenceProps,
  type VeriBusinessIntelligenceSystem as VeriBusinessIntelligenceSystemType,
  VeriAnalyticsScope,
  VeriBusinessContext,
  VeriAIInsight,
  VeriComplianceAnalytics,
  VeriMarketIntelligence
} from '../types';
import { veriBusinessIntelligenceEngine } from '../services/veriBusinessIntelligenceService';
import '../styles/VeriBusinessIntelligence.css';

// Vietnamese Business Intelligence Provider Context
const VeriBusinessIntelligenceContext = React.createContext<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext?: VeriBusinessContext;
  veriAIAnalytics?: any;
} | null>(null);

// Use the same language switcher as Landing page

// Analytics Dashboard Selector Component
const VeriAnalyticsDashboardSelector: React.FC<{
  veriAvailableDashboards: VeriAnalyticsScope[];
  veriActiveDashboard: VeriAnalyticsScope;
  veriOnDashboardSelect: (scope: VeriAnalyticsScope) => void;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriAvailableDashboards, veriActiveDashboard, veriOnDashboardSelect, veriLanguage }) => {
  
  const veriDashboardLabels = {
    vietnamese: {
      'compliance-performance': 'Hiệu suất Tuân thủ',
      'market-positioning': 'Vị trí Thị trường',
      'risk-assessment': 'Đánh giá Rủi ro',
      'operational-efficiency': 'Hiệu quả Vận hành',
      'competitive-analysis': 'Phân tích Cạnh tranh',
      'cultural-alignment': 'Phù hợp Văn hóa',
      'growth-opportunities': 'Cơ hội Tăng trưởng',
      'regulatory-tracking': 'Theo dõi Quy định',
      'stakeholder-insights': 'Góc nhìn Bên liên quan',
      'predictive-analytics': 'Phân tích Dự đoán'
    },
    english: {
      'compliance-performance': 'Compliance Performance',
      'market-positioning': 'Market Positioning',
      'risk-assessment': 'Risk Assessment',
      'operational-efficiency': 'Operational Efficiency',
      'competitive-analysis': 'Competitive Analysis',
      'cultural-alignment': 'Cultural Alignment',
      'growth-opportunities': 'Growth Opportunities',
      'regulatory-tracking': 'Regulatory Tracking',
      'stakeholder-insights': 'Stakeholder Insights',
      'predictive-analytics': 'Predictive Analytics'
    }
  };

  return (
    <div className="veri-dashboard-selector">
      <h3 className="veri-selector-title">
        {veriLanguage === 'vietnamese' ? 'Bảng điều khiển Phân tích' : 'Analytics Dashboards'}
      </h3>
      <div className="veri-dashboard-tabs">
        {veriAvailableDashboards.map((dashboard) => (
          <button
            key={dashboard}
            className={`veri-dashboard-tab ${veriActiveDashboard === dashboard ? 'active' : ''}`}
            onClick={() => veriOnDashboardSelect(dashboard)}
          >
            {veriDashboardLabels[veriLanguage][dashboard]}
          </button>
        ))}
      </div>
    </div>
  );
};

// Business Intelligence Overview Component
const VeriBusinessIntelligenceOverview: React.FC<{
  veriAIInsights?: VeriAIInsight[];
  veriMarketIntelligence?: VeriMarketIntelligence;
  veriComplianceAnalytics?: VeriComplianceAnalytics;
}> = ({ veriAIInsights, veriMarketIntelligence, veriComplianceAnalytics }) => {
  const veriContext = React.useContext(VeriBusinessIntelligenceContext);

  return (
    <div className="veri-business-intelligence-overview">
      <div className="veri-overview-header">
        <h2 className="veri-overview-title">
          {veriContext?.veriLanguage === 'vietnamese' 
            ? 'Tổng quan Thông tin Kinh doanh AI'
            : 'AI Business Intelligence Overview'}
        </h2>
        <div className="veri-ai-status">
          <div className="veri-ai-indicator active">
            <div className="veri-ai-pulse"></div>
            <span>
              {veriContext?.veriLanguage === 'vietnamese' 
                ? 'AI Đang phân tích'
                : 'AI Analyzing'}
            </span>
          </div>
        </div>
      </div>

      <div className="veri-overview-metrics">
        <div className="veri-metric-card">
          <div className="veri-metric-icon compliance">📊</div>
          <div className="veri-metric-content">
            <div className="veri-metric-label">
              {veriContext?.veriLanguage === 'vietnamese' ? 'Điểm Tuân thủ' : 'Compliance Score'}
            </div>
            <div className="veri-metric-value">
              {veriComplianceAnalytics?.veriOverallScore || 0}%
            </div>
            <div className="veri-metric-trend positive">
              ↗ +2.3%
            </div>
          </div>
        </div>

        <div className="veri-metric-card">
          <div className="veri-metric-icon market">📈</div>
          <div className="veri-metric-content">
            <div className="veri-metric-label">
              {veriContext?.veriLanguage === 'vietnamese' ? 'Vị trí Thị trường' : 'Market Position'}
            </div>
            <div className="veri-metric-value">
              {veriMarketIntelligence?.veriCompetitivePosition?.veriCompetitiveRank || 'N/A'}
            </div>
            <div className="veri-metric-trend stable">
              → Stable
            </div>
          </div>
        </div>

        <div className="veri-metric-card">
          <div className="veri-metric-icon insights">🤖</div>
          <div className="veri-metric-content">
            <div className="veri-metric-label">
              {veriContext?.veriLanguage === 'vietnamese' ? 'Góc nhìn AI' : 'AI Insights'}
            </div>
            <div className="veri-metric-value">
              {veriAIInsights?.length || 0}
            </div>
            <div className="veri-metric-trend positive">
              {veriContext?.veriLanguage === 'vietnamese' ? 'Mới' : 'New'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Analytics Content Component
const VeriAnalyticsContent: React.FC<{
  veriAnalyticsScope: VeriAnalyticsScope;
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext?: VeriBusinessContext;
  veriAIInsights?: VeriAIInsight[];
}> = ({ veriAnalyticsScope, veriLanguage, veriBusinessContext, veriAIInsights }) => {
  
  const renderAnalyticsContent = () => {
    switch (veriAnalyticsScope) {
      case 'compliance-performance':
        return <VeriCompliancePerformanceDashboard 
          veriBusinessContext={veriBusinessContext}
          veriLanguage={veriLanguage}
          veriAIAnalytics={null}
        />;
      case 'market-positioning':
        return <VeriMarketPositioningDashboard 
          veriLanguage={veriLanguage}
          veriBusinessContext={veriBusinessContext}
        />;
      case 'predictive-analytics':
        return <VeriPredictiveAnalyticsDashboard 
          veriLanguage={veriLanguage}
          veriAIInsights={veriAIInsights}
        />;
      default:
        return <VeriDefaultAnalyticsDashboard 
          veriScope={veriAnalyticsScope}
          veriLanguage={veriLanguage}
        />;
    }
  };

  return (
    <div className="veri-analytics-content">
      {renderAnalyticsContent()}
    </div>
  );
};

// Compliance Performance Dashboard Component
const VeriCompliancePerformanceDashboard: React.FC<{
  veriBusinessContext?: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriAIAnalytics?: any;
  veriOnInsightAction?: (insight: VeriAIInsight) => void;
}> = ({ veriBusinessContext, veriLanguage, veriAIAnalytics: _veriAIAnalytics, veriOnInsightAction: _veriOnInsightAction }) => {
  
  const [veriComplianceMetrics, setVeriComplianceMetrics] = useState<any>();
  const [veriPerformanceTrends, setVeriPerformanceTrends] = useState<any[]>();
  const [veriRiskAnalysis, setVeriRiskAnalysis] = useState<any>();
  const [veriLoading, setVeriLoading] = useState(true);

  const veriComplianceDashboardContent = {
    vietnamese: {
      veriTitle: "Phân tích Hiệu suất Tuân thủ",
      veriSubtitle: "AI phân tích hiệu suất tuân thủ PDPL 2025 và đưa ra khuyến nghị tối ưu",
      veriDescription: "Hệ thống AI giám sát và phân tích hiệu suất tuân thủ của doanh nghiệp",
      veriMetrics: {
        'overall-compliance': 'Tổng thể Tuân thủ',
        'risk-score': 'Điểm Rủi ro',
        'policy-effectiveness': 'Hiệu quả Chính sách',
        'training-completion': 'Hoàn thành Đào tạo',
        'incident-response': 'Ứng phó Sự cố',
        'audit-readiness': 'Sẵn sàng Kiểm tra',
        'data-governance': 'Quản trị Dữ liệu',
        'cultural-alignment': 'Phù hợp Văn hóa'
      }
    },
    english: {
      veriTitle: "Compliance Performance Analytics",
      veriSubtitle: "AI analyzes PDPL 2025 compliance performance and provides optimization recommendations",
      veriDescription: "AI system monitors and analyzes business compliance performance",
      veriMetrics: {
        'overall-compliance': 'Overall Compliance',
        'risk-score': 'Risk Score',
        'policy-effectiveness': 'Policy Effectiveness',
        'training-completion': 'Training Completion',
        'incident-response': 'Incident Response',
        'audit-readiness': 'Audit Readiness',
        'data-governance': 'Data Governance',
        'cultural-alignment': 'Cultural Alignment'
      }
    }
  };

  useEffect(() => {
    const loadComplianceAnalytics = async () => {
      try {
        setVeriLoading(true);
        
        if (veriBusinessContext) {
          const analytics = await veriBusinessIntelligenceEngine.analyzeCompliancePerformance(
            veriBusinessContext
          );
          setVeriComplianceMetrics(analytics);
        }
        
        // Mock performance trends data
        setVeriPerformanceTrends([
          { veriMonth: 'Jan', veriScore: 78, veriRisk: 22 },
          { veriMonth: 'Feb', veriScore: 82, veriRisk: 18 },
          { veriMonth: 'Mar', veriScore: 85, veriRisk: 15 },
          { veriMonth: 'Apr', veriScore: 88, veriRisk: 12 },
          { veriMonth: 'May', veriScore: 91, veriRisk: 9 },
          { veriMonth: 'Jun', veriScore: 89, veriRisk: 11 }
        ]);

        // Mock risk analysis
        setVeriRiskAnalysis({
          veriCurrentRisk: 11,
          veriTrend: 'decreasing',
          veriTopRisks: [
            'Data Processing Documentation',
            'Employee Training Compliance',
            'Third-party Data Sharing'
          ]
        });

      } catch (error) {
        console.error('Error loading compliance analytics:', error);
      } finally {
        setVeriLoading(false);
      }
    };

    loadComplianceAnalytics();
  }, [veriBusinessContext]);

  if (veriLoading) {
    return (
      <div className="veri-loading-container">
        <div className="veri-loading-spinner"></div>
        <p>{veriLanguage === 'vietnamese' ? 'Đang phân tích dữ liệu tuân thủ...' : 'Analyzing compliance data...'}</p>
      </div>
    );
  }

  return (
    <div className="veri-compliance-analytics-container">
      <div className="veri-analytics-header">
        <h2 className="veri-dashboard-title">
          {veriComplianceDashboardContent[veriLanguage].veriTitle}
        </h2>
        <div className="veri-ai-analytics-indicator">
          <div className="veri-ai-brain active">🤖</div>
          <span className="veri-ai-analytics-text">
            {veriComplianceDashboardContent[veriLanguage].veriDescription}
          </span>
        </div>
      </div>

      <div className="veri-executive-summary">
        <h3 className="veri-summary-header">
          {veriLanguage === 'vietnamese' ? 'Tóm tắt Điều hành AI' : 'AI Executive Summary'}
        </h3>
        
        {veriComplianceMetrics && (
          <div className="veri-executive-insights">
            <div className="veri-overall-compliance-score">
              <div className="veri-score-visualization">
                <div className="veri-score-circle">
                  <div className="veri-score-value">{veriComplianceMetrics.veriOverallScore || 89}%</div>
                  <div className="veri-score-label">
                    {veriComplianceDashboardContent[veriLanguage].veriMetrics['overall-compliance']}
                  </div>
                </div>
              </div>
              <div className="veri-score-insights">
                <div className="veri-score-trend positive">
                  ↗ {veriLanguage === 'vietnamese' ? 'Cải thiện 3.2% trong tháng qua' : 'Improved 3.2% last month'}
                </div>
                <div className="veri-score-benchmark">
                  {veriLanguage === 'vietnamese' 
                    ? 'Cao hơn 78% doanh nghiệp cùng ngành'
                    : '78% higher than industry peers'}
                </div>
              </div>
            </div>

            <div className="veri-key-metrics-grid">
              <div className="veri-metric-item">
                <div className="veri-metric-icon">🛡️</div>
                <div className="veri-metric-info">
                  <div className="veri-metric-value">92%</div>
                  <div className="veri-metric-name">
                    {veriComplianceDashboardContent[veriLanguage].veriMetrics['policy-effectiveness']}
                  </div>
                </div>
              </div>
              
              <div className="veri-metric-item">
                <div className="veri-metric-icon">📚</div>
                <div className="veri-metric-info">
                  <div className="veri-metric-value">87%</div>
                  <div className="veri-metric-name">
                    {veriComplianceDashboardContent[veriLanguage].veriMetrics['training-completion']}
                  </div>
                </div>
              </div>
              
              <div className="veri-metric-item">
                <div className="veri-metric-icon">⚡</div>
                <div className="veri-metric-info">
                  <div className="veri-metric-value">94%</div>
                  <div className="veri-metric-name">
                    {veriComplianceDashboardContent[veriLanguage].veriMetrics['incident-response']}
                  </div>
                </div>
              </div>
              
              <div className="veri-metric-item">
                <div className="veri-metric-icon">✅</div>
                <div className="veri-metric-info">
                  <div className="veri-metric-value">91%</div>
                  <div className="veri-metric-name">
                    {veriComplianceDashboardContent[veriLanguage].veriMetrics['audit-readiness']}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="veri-performance-trend-analysis">
        <h4 className="veri-trend-analysis-header">
          {veriLanguage === 'vietnamese' ? 'Phân tích Xu hướng Hiệu suất' : 'Performance Trend Analysis'}
        </h4>
        
        <div className="veri-trend-charts">
          <div className="veri-compliance-trend-chart">
            <h5>{veriLanguage === 'vietnamese' ? 'Xu hướng Điểm Tuân thủ' : 'Compliance Score Trend'}</h5>
            <div className="veri-chart-container">
              {veriPerformanceTrends?.map((trend, index) => (
                <div key={index} className="veri-trend-bar">
                  <div 
                    className="veri-trend-fill"
                    style={{ height: `${trend.veriScore}%` }}
                  ></div>
                  <span className="veri-trend-label">{trend.veriMonth}</span>
                  <span className="veri-trend-value">{trend.veriScore}%</span>
                </div>
              ))}
            </div>
          </div>

          <div className="veri-risk-trend-chart">
            <h5>{veriLanguage === 'vietnamese' ? 'Xu hướng Điểm Rủi ro' : 'Risk Score Trend'}</h5>
            <div className="veri-risk-summary">
              <div className="veri-current-risk">
                <span className="veri-risk-value">{veriRiskAnalysis?.veriCurrentRisk}%</span>
                <span className="veri-risk-label">
                  {veriLanguage === 'vietnamese' ? 'Rủi ro Hiện tại' : 'Current Risk'}
                </span>
              </div>
              <div className="veri-risk-trend">
                <span className="veri-trend-indicator decreasing">↓</span>
                <span>{veriLanguage === 'vietnamese' ? 'Đang giảm' : 'Decreasing'}</span>
              </div>
            </div>
            <div className="veri-top-risks">
              <h6>{veriLanguage === 'vietnamese' ? 'Rủi ro Hàng đầu' : 'Top Risks'}</h6>
              <ul>
                {veriRiskAnalysis?.veriTopRisks?.map((risk: string, index: number) => (
                  <li key={index} className="veri-risk-item">
                    <span className="veri-risk-indicator">⚠️</span>
                    <span>{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="veri-analytics-actions">
        <button className="veri-export-report-button">
          {veriLanguage === 'vietnamese' ? 'Xuất Báo cáo' : 'Export Report'}
        </button>
        <button className="veri-schedule-analysis-button">
          {veriLanguage === 'vietnamese' ? 'Lên lịch Phân tích' : 'Schedule Analysis'}
        </button>
        <button className="veri-ai-recommendations-button">
          {veriLanguage === 'vietnamese' ? 'Khuyến nghị AI' : 'AI Recommendations'}
        </button>
      </div>
    </div>
  );
};

// Market Positioning Dashboard Component
const VeriMarketPositioningDashboard: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext?: VeriBusinessContext;
}> = ({ veriLanguage, veriBusinessContext: _veriBusinessContext }) => {
  return (
    <div className="veri-market-positioning-container">
      <h2>{veriLanguage === 'vietnamese' ? 'Phân tích Vị trí Thị trường' : 'Market Positioning Analysis'}</h2>
      <p>{veriLanguage === 'vietnamese' 
        ? 'Đang phát triển bảng điều khiển phân tích vị trí thị trường...'
        : 'Market positioning analytics dashboard under development...'}</p>
    </div>
  );
};

// Predictive Analytics Dashboard Component
const VeriPredictiveAnalyticsDashboard: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriAIInsights?: VeriAIInsight[];
}> = ({ veriLanguage, veriAIInsights: _veriAIInsights }) => {
  return (
    <div className="veri-predictive-analytics-container">
      <h2>{veriLanguage === 'vietnamese' ? 'Phân tích Dự đoán AI' : 'AI Predictive Analytics'}</h2>
      <p>{veriLanguage === 'vietnamese' 
        ? 'Đang phát triển bảng điều khiển phân tích dự đoán AI...'
        : 'AI predictive analytics dashboard under development...'}</p>
    </div>
  );
};

// Default Analytics Dashboard Component
const VeriDefaultAnalyticsDashboard: React.FC<{
  veriScope: VeriAnalyticsScope;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriScope, veriLanguage }) => {
  return (
    <div className="veri-default-analytics-container">
      <h2>{veriLanguage === 'vietnamese' ? `Phân tích ${veriScope}` : `${veriScope} Analytics`}</h2>
      <p>{veriLanguage === 'vietnamese' 
        ? 'Bảng điều khiển này đang được phát triển...'
        : 'This dashboard is under development...'}</p>
    </div>
  );
};

// Analytics Layout Component
const VeriAnalyticsLayout: React.FC<{
  children: React.ReactNode;
  veriCulturalStyle?: 'north' | 'central' | 'south';
}> = ({ children, veriCulturalStyle = 'north' }) => {
  return (
    <div className={`veri-analytics-layout ${veriCulturalStyle}`}>
      <div className="veri-analytics-container">
        {children}
      </div>
    </div>
  );
};

// Business Intelligence Provider Component
const VeriBusinessIntelligenceProvider: React.FC<{
  children: React.ReactNode;
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext?: VeriBusinessContext;
  veriAIAnalytics?: any;
}> = ({ children, veriLanguage, veriBusinessContext, veriAIAnalytics }) => {
  return (
    <VeriBusinessIntelligenceContext.Provider 
      value={{ veriLanguage, veriBusinessContext, veriAIAnalytics }}
    >
      {children}
    </VeriBusinessIntelligenceContext.Provider>
  );
};

// Helper function to get available dashboards
const getVeriAvailableDashboards = (_veriBusinessContext?: VeriBusinessContext): VeriAnalyticsScope[] => {
  // All available dashboards - can be filtered based on business context
  return [
    'compliance-performance',
    'market-positioning', 
    'risk-assessment',
    'operational-efficiency',
    'competitive-analysis',
    'cultural-alignment',
    'growth-opportunities',
    'regulatory-tracking',
    'stakeholder-insights',
    'predictive-analytics'
  ];
};

// Main Vietnamese Business Intelligence System Component
export const VeriBusinessIntelligenceSystem: React.FC<VeriBusinessIntelligenceProps> = ({
  veriBusinessContext,
  veriInitialScope = 'compliance-performance',
  veriOnAnalyticsUpdate,
  veriOnInsightAction: _veriOnInsightAction,
  veriOnRecommendationAction: _veriOnRecommendationAction
}) => {
  const [veriAnalyticsState, setVeriAnalyticsState] = useState<VeriBusinessIntelligenceSystemType>();
  const [veriActiveDashboard, setVeriActiveDashboard] = useState<VeriAnalyticsScope>(veriInitialScope);
  const [_veriAIAnalytics, _setVeriAIAnalytics] = useState<any>();
  const [veriLoading, setVeriLoading] = useState(true);

  // Use global language switcher
  const { switchLanguage, isVietnamese } = useLanguageSwitch();
  // Map i18n language to BI language
  const veriLanguage = isVietnamese ? 'vietnamese' : 'english';

  // Initialize business intelligence system
  useEffect(() => {
    const initializeBusinessIntelligence = async () => {
      try {
        setVeriLoading(true);
        
        if (veriBusinessContext) {
          const intelligenceSystem = await veriBusinessIntelligenceEngine.generateBusinessIntelligence(
            veriBusinessContext
          );
          
          setVeriAnalyticsState(intelligenceSystem);
          
          if (veriOnAnalyticsUpdate) {
            veriOnAnalyticsUpdate(intelligenceSystem);
          }
        }
      } catch (error) {
        console.error('Error initializing business intelligence:', error);
      } finally {
        setVeriLoading(false);
      }
    };

    initializeBusinessIntelligence();
  }, [veriBusinessContext, veriOnAnalyticsUpdate]);

  if (veriLoading) {
    return (
      <div className="veri-bi-loading-container">
        <div className="veri-loading-spinner"></div>
        <h3>{veriLanguage === 'vietnamese' 
          ? 'Đang khởi tạo Hệ thống Thông tin Kinh doanh AI...'
          : 'Initializing AI Business Intelligence System...'}</h3>
        <p>{veriLanguage === 'vietnamese' 
          ? 'Phân tích dữ liệu và tạo báo cáo thông minh...'
          : 'Analyzing data and generating intelligent insights...'}</p>
      </div>
    );
  }

  return (
    <VeriBusinessIntelligenceProvider
      veriLanguage={veriLanguage}
      veriBusinessContext={veriBusinessContext}
      veriAIAnalytics={_veriAIAnalytics}
    >
      <div className="min-h-screen" style={{ background: 'linear-gradient(135deg, #f0f4f0 0%, #e8ede8 100%)' }}>
        {/* Use shared VeriSyntraBanner component */}
        <VeriSyntraBanner
          variant="portal"
          currentLanguage={isVietnamese ? 'vi' : 'en'}
          onLanguageChange={(lang) => switchLanguage(lang)}
          showConnectionStatus={false}
          showLanguageToggle={true}
          customTitle="VeriSyntra"
          customSubtitle={veriLanguage === 'vietnamese' 
            ? 'Hệ thống Thông tin Kinh doanh AI' 
            : 'AI Business Intelligence System'}
        />
        
        <VeriAnalyticsLayout veriCulturalStyle={veriBusinessContext?.veriRegionalLocation}>
          <VeriAnalyticsDashboardSelector
            veriAvailableDashboards={getVeriAvailableDashboards(veriBusinessContext)}
            veriActiveDashboard={veriActiveDashboard}
            veriOnDashboardSelect={setVeriActiveDashboard}
            veriLanguage={veriLanguage}
          />
          <VeriBusinessIntelligenceOverview
            veriAIInsights={veriAnalyticsState?.veriAIInsights}
            veriMarketIntelligence={veriAnalyticsState?.veriMarketIntelligence}
            veriComplianceAnalytics={veriAnalyticsState?.veriComplianceAnalytics}
          />
          <VeriAnalyticsContent
            veriAnalyticsScope={veriActiveDashboard}
            veriLanguage={veriLanguage}
            veriBusinessContext={veriBusinessContext}
            veriAIInsights={veriAnalyticsState?.veriAIInsights}
          />
        </VeriAnalyticsLayout>
      </div>
    </VeriBusinessIntelligenceProvider>
  );
};

export default VeriBusinessIntelligenceSystem;