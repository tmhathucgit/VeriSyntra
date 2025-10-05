// VeriPortal System Integration Hub - Main Component
// AI-powered comprehensive system integration platform for Vietnamese businesses

import React, { useState, useEffect } from 'react';
import VeriSyntraBanner from '../../../shared/VeriSyntraBanner';
import { useLanguageSwitch } from '../../../../hooks/useCulturalIntelligence';
import { usePageTitle } from '../../../../hooks/usePageTitle';
import type {
  VeriSystemsEcosystem,
  VeriIntegrationView,
  VeriSystemsStatus,
  VeriIntegrationInsight,
  VeriIntegrationHealth,
  VeriGovernmentConnection,
  VeriMPSIntegration,
  VeriBusinessContext,
  VeriSystemStatus,
  VeriSystemInfo
} from '../types/VeriSystemIntegrationTypes';
import {
  analyzeVeriSystemsEcosystem,
  generateVeriEcosystemMetrics,
  generateVeriIntegrationInsights,
  generateVeriIntegrationHealth,
  generateVeriGovernmentConnections,
  generateVeriMPSIntegration,
  manageVeriSystem,
  viewVeriSystemDetails,
  monitorVeriFlow,
  runVeriSystemsHealthCheck,
  launchVeriIntegrationWizard,
  generateVeriSystemsReport,
  configureVeriService,
  enableVeriService
} from '../services/veriSystemIntegrationEngine';
import '../styles/VeriSystemIntegration.css';

// Mock Systems Ecosystem
const createMockSystemsEcosystem = (): VeriSystemsEcosystem => {
  const createSystemInfo = (
    id: string,
    nameVi: string,
    nameEn: string,
    type: string
  ): VeriSystemInfo => ({
    veriSystemId: id,
    veriSystemName: { vietnamese: nameVi, english: nameEn },
    veriSystemType: type,
    veriStatus: 'healthy' as VeriSystemStatus,
    veriUptime: 99.5,
    veriPerformance: 95,
    veriIntegrations: 5,
    veriVersion: '1.0.0',
    veriLastHealthCheck: new Date()
  });

  return {
    veriPortal: createSystemInfo('veri-portal', 'VeriPortal - Cổng Khách hàng', 'VeriPortal - Customer Portal', 'customer-portal'),
    veriCompliance: createSystemInfo('veri-compliance', 'VeriCompliance - Tuân thủ', 'VeriCompliance - Compliance', 'compliance'),
    veriTraining: createSystemInfo('veri-training', 'VeriTraining - Đào tạo', 'VeriTraining - Training', 'training'),
    veriAnalytics: createSystemInfo('veri-analytics', 'VeriAnalytics - Phân tích', 'VeriAnalytics - Analytics', 'analytics'),
    veriCultural: createSystemInfo('veri-cultural', 'VeriCultural - Văn hóa', 'VeriCultural - Cultural', 'cultural'),
    veriSecurity: createSystemInfo('veri-security', 'VeriSecurity - Bảo mật', 'VeriSecurity - Security', 'security'),
    veriGovernment: createSystemInfo('veri-government', 'VeriGovernment - Chính phủ', 'VeriGovernment - Government', 'government'),
    veriThirdParty: [],
    veriBusinessSystems: []
  };
};

// Mock Business Context
const createMockBusinessContext = (): VeriBusinessContext => ({
  veriBusinessId: 'BUSINESS-VN-001',
  veriBusinessName: 'Vietnamese Enterprise Corp',
  veriRegionalLocation: 'south',
  veriIndustry: 'technology',
  veriSize: 'medium',
  veriComplianceRequirements: ['PDPL-2025', 'ISO-27001', 'SOC2']
});

export const VeriSystemIntegrationSystem: React.FC = () => {
  const { isVietnamese } = useLanguageSwitch();
  const language = isVietnamese ? 'vietnamese' : 'english';
  
  // Set page title
  usePageTitle({ 
    title: 'System Integration', 
    titleVi: 'Tích hợp Hệ thống' 
  });

  const [veriActiveView, setVeriActiveView] = useState<VeriIntegrationView>('ecosystem-overview');
  const [veriSystemsEcosystem] = useState<VeriSystemsEcosystem>(createMockSystemsEcosystem());
  const [veriBusinessContext] = useState<VeriBusinessContext>(createMockBusinessContext());
  const [veriSystemsStatus, setVeriSystemsStatus] = useState<VeriSystemsStatus>();
  const [veriIntegrationInsights, setVeriIntegrationInsights] = useState<VeriIntegrationInsight[]>();
  const [veriIntegrationHealth, setVeriIntegrationHealth] = useState<VeriIntegrationHealth>();
  const [veriGovernmentConnections, setVeriGovernmentConnections] = useState<VeriGovernmentConnection[]>();
  const [veriMPSIntegration, setVeriMPSIntegration] = useState<VeriMPSIntegration>();
  const [veriLoading, setVeriLoading] = useState(true);

  // Content translations
  const content = {
    vietnamese: {
      title: 'Tích hợp Hệ thống VeriSyntra',
      subtitle: 'Nền tảng điều phối tích hợp toàn diện với AI',
      description: 'AI điều phối tất cả hệ thống VeriSyntra cho doanh nghiệp Việt Nam',
      
      views: {
        'ecosystem-overview': 'Tổng quan Hệ sinh thái',
        'government-integration': 'Tích hợp Chính phủ',
        'data-flows': 'Luồng Dữ liệu',
        'orchestration-ai': 'AI Điều phối',
        'health-monitoring': 'Giám sát Sức khỏe',
        'cultural-bridge': 'Cầu nối Văn hóa'
      },

      ecosystemTitle: 'Hệ sinh thái VeriSystems',
      ecosystemSubtitle: 'Quản lý tích hợp toàn diện với AI điều phối',
      
      healthMetrics: {
        overall: 'Tình trạng Tổng thể',
        activeIntegrations: 'Tích hợp Hoạt động',
        dataFlow: 'Luồng Dữ liệu'
      },

      healthStatus: {
        healthy: 'Khỏe mạnh',
        warning: 'Cảnh báo',
        critical: 'Nghiêm trọng',
        offline: 'Ngoại tuyến'
      },

      systemMetrics: {
        uptime: 'Uptime',
        performance: 'Hiệu suất',
        integrations: 'Tích hợp'
      },

      actions: {
        manage: 'Quản lý',
        details: 'Chi tiết',
        monitor: 'Giám sát',
        healthCheck: 'Kiểm tra Sức khỏe Hệ thống',
        integrationWizard: 'Trình hướng dẫn Tích hợp',
        systemsReport: 'Báo cáo Hệ thống'
      },

      dataFlows: {
        title: 'Luồng Tích hợp Dữ liệu',
        volume: 'Khối lượng',
        latency: 'Độ trễ',
        health: 'Sức khỏe'
      },

      government: {
        title: 'Tích hợp Hệ thống Chính phủ',
        subtitle: 'Kết nối an toàn với các cơ quan Chính phủ Việt Nam',
        mpsTitle: 'Bộ Công an - Tích hợp PDPL',
        capabilities: 'Khả năng',
        dataReporting: 'Báo cáo Dữ liệu',
        incidentNotification: 'Thông báo Sự cố',
        complianceVerification: 'Xác minh Tuân thủ',
        configuration: 'Cấu hình Kết nối MPS',
        regulatorySync: 'Đồng bộ Tuân thủ Quy định',
        configure: 'Cấu hình',
        enable: 'Kích hoạt'
      },

      loading: 'Đang tải hệ thống tích hợp...'
    },
    english: {
      title: 'VeriSyntra System Integration',
      subtitle: 'Comprehensive integration orchestration platform with AI',
      description: 'AI orchestrates all VeriSyntra systems for Vietnamese businesses',
      
      views: {
        'ecosystem-overview': 'Ecosystem Overview',
        'government-integration': 'Government Integration',
        'data-flows': 'Data Flows',
        'orchestration-ai': 'AI Orchestration',
        'health-monitoring': 'Health Monitoring',
        'cultural-bridge': 'Cultural Bridge'
      },

      ecosystemTitle: 'VeriSystems Ecosystem',
      ecosystemSubtitle: 'Comprehensive integration management with AI orchestration',
      
      healthMetrics: {
        overall: 'Overall Health',
        activeIntegrations: 'Active Integrations',
        dataFlow: 'Data Flow'
      },

      healthStatus: {
        healthy: 'Healthy',
        warning: 'Warning',
        critical: 'Critical',
        offline: 'Offline'
      },

      systemMetrics: {
        uptime: 'Uptime',
        performance: 'Performance',
        integrations: 'Integrations'
      },

      actions: {
        manage: 'Manage',
        details: 'Details',
        monitor: 'Monitor',
        healthCheck: 'Run Systems Health Check',
        integrationWizard: 'Integration Wizard',
        systemsReport: 'Systems Report'
      },

      dataFlows: {
        title: 'Integration Data Flows',
        volume: 'Volume',
        latency: 'Latency',
        health: 'Health'
      },

      government: {
        title: 'Government Systems Integration',
        subtitle: 'Secure connection with Vietnamese Government agencies',
        mpsTitle: 'Ministry of Public Security - PDPL Integration',
        capabilities: 'Capabilities',
        dataReporting: 'Data Reporting',
        incidentNotification: 'Incident Notification',
        complianceVerification: 'Compliance Verification',
        configuration: 'MPS Connection Configuration',
        regulatorySync: 'Regulatory Compliance Sync',
        configure: 'Configure',
        enable: 'Enable'
      },

      loading: 'Loading system integration...'
    }
  };

  // Load integration data
  useEffect(() => {
    const loadIntegrationData = async () => {
      setVeriLoading(true);
      try {
        // Load all integration data in parallel
        const [status, health, insights, govConnections, mpsIntegration] = await Promise.all([
          analyzeVeriSystemsEcosystem(veriSystemsEcosystem),
          generateVeriIntegrationHealth(),
          generateVeriIntegrationInsights(veriSystemsEcosystem, language),
          generateVeriGovernmentConnections(veriBusinessContext),
          generateVeriMPSIntegration()
        ]);

        setVeriSystemsStatus(status);
        setVeriIntegrationHealth(health);
        setVeriIntegrationInsights(insights);
        setVeriGovernmentConnections(govConnections);
        setVeriMPSIntegration(mpsIntegration);

        // Generate ecosystem metrics (for future use)
        generateVeriEcosystemMetrics(status);
      } catch (error) {
        console.error('Error loading integration data:', error);
      } finally {
        setVeriLoading(false);
      }
    };

    loadIntegrationData();
  }, [veriSystemsEcosystem, veriBusinessContext, language]);

  const getHealthStatusClass = (status: VeriSystemStatus | undefined): string => {
    if (!status) return 'veri-status-unknown';
    return `veri-status-${status}`;
  };

  const getHealthStatusIcon = (status: VeriSystemStatus | undefined): string => {
    if (!status) return '❓';
    switch (status) {
      case 'healthy': return '✅';
      case 'warning': return '⚠️';
      case 'critical': return '🚨';
      case 'offline': return '🔴';
      default: return '❓';
    }
  };

  if (veriLoading) {
    return (
      <div className="veri-system-integration-container">
        <VeriSyntraBanner variant="portal" />
        <div className="veri-system-integration-loading">
          <div className="veri-lotus-spinner"></div>
          <p className="veri-loading-text">{content[language].loading}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="veri-system-integration-container">
      <VeriSyntraBanner variant="portal" />

      <div className="veri-system-integration-content">
        {/* Header with AI Orchestration Indicator */}
        <div className="veri-integration-header">
          <div className="veri-integration-title-section">
            <h1 className="veri-integration-title">{content[language].title}</h1>
            <p className="veri-integration-subtitle">{content[language].subtitle}</p>
          </div>
          <div className="veri-ai-orchestration-indicator">
            <div className="veri-ai-brain veri-orchestrating"></div>
            <span className="veri-orchestration-text">{content[language].description}</span>
          </div>
        </div>

        {/* View Selector */}
        <div className="veri-integration-view-selector">
          {(Object.keys(content[language].views) as VeriIntegrationView[]).map((view) => (
            <button
              key={view}
              className={`veri-view-button ${veriActiveView === view ? 'veri-view-active' : ''}`}
              onClick={() => setVeriActiveView(view)}
            >
              {content[language].views[view]}
            </button>
          ))}
        </div>

        {/* Ecosystem Overview */}
        {veriActiveView === 'ecosystem-overview' && (
          <div className="veri-ecosystem-overview">
            {/* Health Summary */}
            <div className="veri-health-summary">
              <div className="veri-health-metric">
                <span className="veri-metric-label">{content[language].healthMetrics.overall}</span>
                <div className="veri-health-score">
                  <span className="veri-score-value">{veriIntegrationHealth?.veriOverallScore.toFixed(1)}%</span>
                  <span className={`veri-health-trend veri-trend-${veriIntegrationHealth?.veriHealthTrend}`}>
                    {veriIntegrationHealth?.veriHealthTrend === 'improving' && '📈'}
                    {veriIntegrationHealth?.veriHealthTrend === 'stable' && '➡️'}
                    {veriIntegrationHealth?.veriHealthTrend === 'declining' && '📉'}
                  </span>
                </div>
              </div>

              <div className="veri-health-metric">
                <span className="veri-metric-label">{content[language].healthMetrics.activeIntegrations}</span>
                <div className="veri-integration-count">
                  <span className="veri-count-value">{veriIntegrationHealth?.veriActiveIntegrations}</span>
                  <span className={getHealthStatusClass(veriIntegrationHealth?.veriIntegrationHealth)}>
                    {getHealthStatusIcon(veriIntegrationHealth?.veriIntegrationHealth)}
                  </span>
                </div>
              </div>

              <div className="veri-health-metric">
                <span className="veri-metric-label">{content[language].healthMetrics.dataFlow}</span>
                <div className="veri-data-flow-rate">
                  <span className="veri-flow-value">{veriIntegrationHealth?.veriDataFlowRate.toFixed(0)} MB/s</span>
                  <span className={getHealthStatusClass(veriIntegrationHealth?.veriDataFlowHealth)}>
                    {getHealthStatusIcon(veriIntegrationHealth?.veriDataFlowHealth)}
                  </span>
                </div>
              </div>
            </div>

            {/* Systems Grid */}
            <div className="veri-systems-grid">
              <h2 className="veri-systems-grid-title">{content[language].ecosystemTitle}</h2>
              {Object.entries(veriSystemsEcosystem).slice(0, 8).map(([key, system]) => {
                if (!system || Array.isArray(system)) return null;
                const systemKey = `veri-${key.replace('veri', '').toLowerCase()}`;
                const systemStatus = veriSystemsStatus?.[systemKey];
                
                return (
                  <div key={key} className="veri-system-card">
                    <div className="veri-system-header">
                      <div className="veri-system-icon">{getHealthStatusIcon(systemStatus?.veriStatus)}</div>
                      <h3 className="veri-system-title">{system.veriSystemName[language]}</h3>
                      <span className={`veri-system-status ${getHealthStatusClass(systemStatus?.veriStatus)}`}>
                        {content[language].healthStatus[systemStatus?.veriStatus || 'healthy']}
                      </span>
                    </div>

                    <div className="veri-system-metrics">
                      <div className="veri-system-metric">
                        <span className="veri-metric-label">{content[language].systemMetrics.uptime}</span>
                        <span className="veri-metric-value">{systemStatus?.veriUptime.toFixed(1)}%</span>
                      </div>
                      <div className="veri-system-metric">
                        <span className="veri-metric-label">{content[language].systemMetrics.performance}</span>
                        <div className="veri-performance-bar">
                          <div 
                            className="veri-performance-fill"
                            style={{ width: `${systemStatus?.veriPerformance || 0}%` }}
                          ></div>
                        </div>
                      </div>
                      <div className="veri-system-metric">
                        <span className="veri-metric-label">{content[language].systemMetrics.integrations}</span>
                        <span className="veri-metric-value">{systemStatus?.veriIntegrations}</span>
                      </div>
                    </div>

                    {/* System Insights */}
                    <div className="veri-system-insights">
                      {veriIntegrationInsights
                        ?.filter(insight => insight.veriSystemId === systemKey)
                        ?.slice(0, 2)
                        ?.map((insight, index) => (
                        <div key={index} className={`veri-system-insight veri-insight-${insight.veriInsightType}`}>
                          <span className="veri-insight-icon">
                            {insight.veriInsightType === 'optimization' && '⚡'}
                            {insight.veriInsightType === 'warning' && '⚠️'}
                            {insight.veriInsightType === 'recommendation' && '💡'}
                            {insight.veriInsightType === 'alert' && '🚨'}
                          </span>
                          <span className="veri-insight-text">{insight.veriDescription[language]}</span>
                        </div>
                      ))}
                    </div>

                    <div className="veri-system-actions">
                      <button 
                        className="veri-manage-button"
                        onClick={() => manageVeriSystem(systemKey)}
                      >
                        {content[language].actions.manage}
                      </button>
                      <button 
                        className="veri-details-button"
                        onClick={() => viewVeriSystemDetails(systemKey)}
                      >
                        {content[language].actions.details}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Data Flows */}
            <div className="veri-data-flows-section">
              <h2 className="veri-data-flows-title">{content[language].dataFlows.title}</h2>
              <div className="veri-data-flows-grid">
                {veriIntegrationHealth?.veriDataFlows?.map((flow) => (
                  <div key={flow.veriFlowId} className="veri-data-flow-card">
                    <div className="veri-flow-path">
                      <span className="veri-source-system">{flow.veriSourceSystem}</span>
                      <span className="veri-flow-arrow">{flow.veriDirection === 'bidirectional' ? '↔' : '→'}</span>
                      <span className="veri-target-system">{flow.veriTargetSystem}</span>
                    </div>

                    <div className="veri-flow-metrics">
                      <div className="veri-flow-metric">
                        <span className="veri-metric-label">{content[language].dataFlows.volume}</span>
                        <span className="veri-metric-value">{flow.veriDataVolume}</span>
                      </div>
                      <div className="veri-flow-metric">
                        <span className="veri-metric-label">{content[language].dataFlows.latency}</span>
                        <span className="veri-metric-value">{flow.veriLatency}ms</span>
                      </div>
                      <div className="veri-flow-metric">
                        <span className="veri-metric-label">{content[language].dataFlows.health}</span>
                        <span className={getHealthStatusClass(flow.veriHealth)}>
                          {getHealthStatusIcon(flow.veriHealth)}
                        </span>
                      </div>
                    </div>

                    <button 
                      className="veri-monitor-button"
                      onClick={() => monitorVeriFlow(flow)}
                    >
                      {content[language].actions.monitor}
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Ecosystem Actions */}
            <div className="veri-ecosystem-actions">
              <button 
                className="veri-action-button veri-health-check-button"
                onClick={runVeriSystemsHealthCheck}
              >
                {content[language].actions.healthCheck}
              </button>
              <button 
                className="veri-action-button veri-wizard-button"
                onClick={launchVeriIntegrationWizard}
              >
                {content[language].actions.integrationWizard}
              </button>
              <button 
                className="veri-action-button veri-report-button"
                onClick={generateVeriSystemsReport}
              >
                {content[language].actions.systemsReport}
              </button>
            </div>
          </div>
        )}

        {/* Government Integration View */}
        {veriActiveView === 'government-integration' && (
          <div className="veri-government-integration">
            <div className="veri-government-header">
              <h2 className="veri-government-title">{content[language].government.title}</h2>
              <p className="veri-government-subtitle">{content[language].government.subtitle}</p>
            </div>

            {/* MPS Integration Panel */}
            <div className="veri-mps-integration-panel">
              <div className="veri-mps-header">
                <div className="veri-mps-logo">🏛️</div>
                <h3 className="veri-mps-title">{content[language].government.mpsTitle}</h3>
                <span className={`veri-mps-status veri-status-${veriMPSIntegration?.veriConnectionStatus}`}>
                  {veriMPSIntegration?.veriConnectionStatus === 'connected' ? '🟢' : '🟡'}
                </span>
              </div>

              <div className="veri-mps-capabilities">
                <h4 className="veri-capabilities-title">{content[language].government.capabilities}</h4>
                <div className="veri-capability-grid">
                  <div className={`veri-capability ${veriMPSIntegration?.veriDataReporting ? 'veri-enabled' : 'veri-disabled'}`}>
                    <span className="veri-capability-icon">📊</span>
                    <span className="veri-capability-label">{content[language].government.dataReporting}</span>
                    <span className="veri-capability-status">{veriMPSIntegration?.veriDataReporting ? '✅' : '❌'}</span>
                  </div>
                  <div className={`veri-capability ${veriMPSIntegration?.veriIncidentNotification ? 'veri-enabled' : 'veri-disabled'}`}>
                    <span className="veri-capability-icon">🚨</span>
                    <span className="veri-capability-label">{content[language].government.incidentNotification}</span>
                    <span className="veri-capability-status">{veriMPSIntegration?.veriIncidentNotification ? '✅' : '❌'}</span>
                  </div>
                  <div className={`veri-capability ${veriMPSIntegration?.veriComplianceVerification ? 'veri-enabled' : 'veri-disabled'}`}>
                    <span className="veri-capability-icon">✅</span>
                    <span className="veri-capability-label">{content[language].government.complianceVerification}</span>
                    <span className="veri-capability-status">{veriMPSIntegration?.veriComplianceVerification ? '✅' : '❌'}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Regulatory Agencies */}
            <div className="veri-regulatory-agencies">
              <h3 className="veri-agencies-title">{content[language].government.regulatorySync}</h3>
              <div className="veri-agencies-grid">
                {veriGovernmentConnections?.map((connection) => (
                  <div key={connection.veriConnectionId} className="veri-agency-card">
                    <div className="veri-agency-header">
                      <div className="veri-agency-logo">🏛️</div>
                      <h4 className="veri-agency-name">{connection.veriAgencyName[language]}</h4>
                      <span className={`veri-connection-status veri-status-${connection.veriConnectionStatus}`}>
                        {connection.veriConnectionStatus === 'connected' ? '🟢' : '🟡'}
                      </span>
                    </div>

                    <div className="veri-agency-services">
                      {connection.veriAvailableServices?.map((service) => (
                        <div key={service.veriServiceId} className="veri-agency-service">
                          <span className="veri-service-name">{service.veriServiceName[language]}</span>
                          <span className="veri-service-status">{service.veriEnabled ? '✅' : '❌'}</span>
                          <button
                            className={`veri-service-button ${service.veriEnabled ? 'veri-configure' : 'veri-enable'}`}
                            onClick={() => service.veriEnabled ? configureVeriService(service) : enableVeriService(service)}
                          >
                            {service.veriEnabled ? content[language].government.configure : content[language].government.enable}
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Other views placeholder */}
        {veriActiveView !== 'ecosystem-overview' && veriActiveView !== 'government-integration' && (
          <div className="veri-view-placeholder">
            <h2>{content[language].views[veriActiveView]}</h2>
            <p>This view is under development.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VeriSystemIntegrationSystem;
