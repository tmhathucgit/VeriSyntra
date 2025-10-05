// VeriPortal System Integration Types - Vietnamese Business System Integration
// Designed for Vietnamese businesses to achieve comprehensive system integration and orchestration

export type VeriLanguage = 'vietnamese' | 'english';

export type VeriIntegrationView = 
  | 'ecosystem-overview' 
  | 'government-integration' 
  | 'data-flows' 
  | 'orchestration-ai' 
  | 'health-monitoring'
  | 'cultural-bridge';

export type VeriSystemStatus = 'healthy' | 'warning' | 'critical' | 'offline';

export type VeriConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'error';

export type VeriHealthTrend = 'improving' | 'stable' | 'declining' | 'critical';

export type VeriSecurityLevel = 'maximum' | 'high' | 'medium' | 'standard';

export type VeriRegionalLocation = 'north' | 'central' | 'south';

// Core Vietnamese System Integration Hub
export interface VeriSystemIntegrationHub {
  veriIntegrationId: string;
  veriSystemsEcosystem: VeriSystemsEcosystem;
  veriIntegrationTopology: VeriIntegrationTopology;
  veriDataFlows: VeriDataFlow[];
  veriLanguagePreference: VeriLanguage;
  veriCulturalIntegration: VeriCulturalIntegration;
  veriOrchestrationEngine: VeriOrchestrationEngine;
  veriAICoordination: VeriAICoordination;
  veriIntegrationHealth: VeriIntegrationHealth;
}

// Vietnamese Systems Ecosystem
export interface VeriSystemsEcosystem {
  veriPortal: VeriSystemInfo;
  veriCompliance: VeriSystemInfo;
  veriTraining: VeriSystemInfo;
  veriAnalytics: VeriSystemInfo;
  veriCultural: VeriSystemInfo;
  veriSecurity: VeriSystemInfo;
  veriGovernment: VeriSystemInfo;
  veriThirdParty: VeriSystemInfo[];
  veriBusinessSystems: VeriSystemInfo[];
}

// Individual System Information
export interface VeriSystemInfo {
  veriSystemId: string;
  veriSystemName: { vietnamese: string; english: string };
  veriSystemType: string;
  veriStatus: VeriSystemStatus;
  veriUptime: number;
  veriPerformance: number;
  veriIntegrations: number;
  veriVersion: string;
  veriLastHealthCheck: Date;
}

// Vietnamese Integration Topology
export interface VeriIntegrationTopology {
  veriCoreIntegrations: VeriCoreIntegration[];
  veriDataPipelines: VeriDataPipeline[];
  veriAPIConnections: VeriAPIConnection[];
  veriEventStreams: VeriEventStream[];
  veriCulturalBridges: VeriCulturalBridge[];
  veriBusinessWorkflows: VeriBusinessWorkflow[];
  veriGovernmentConnections: VeriGovernmentConnection[];
}

// Core System Integration
export interface VeriCoreIntegration {
  veriIntegrationId: string;
  veriSourceSystem: string;
  veriTargetSystem: string;
  veriIntegrationType: string;
  veriStatus: VeriConnectionStatus;
  veriDataFlowRate: number;
  veriLatency: number;
  veriHealth: VeriSystemStatus;
}

// Data Pipeline
export interface VeriDataPipeline {
  veriPipelineId: string;
  veriPipelineName: { vietnamese: string; english: string };
  veriSourceSystems: string[];
  veriTargetSystems: string[];
  veriDataVolume: string;
  veriProcessingRate: number;
  veriStatus: VeriSystemStatus;
}

// API Connection
export interface VeriAPIConnection {
  veriConnectionId: string;
  veriEndpoint: string;
  veriMethod: string;
  veriStatus: VeriConnectionStatus;
  veriRequestRate: number;
  veriSuccessRate: number;
  veriAverageLatency: number;
}

// Event Stream
export interface VeriEventStream {
  veriStreamId: string;
  veriStreamName: { vietnamese: string; english: string };
  veriEventType: string;
  veriEventRate: number;
  veriSubscribers: number;
  veriStatus: VeriSystemStatus;
}

// Cultural Bridge
export interface VeriCulturalBridge {
  veriBridgeId: string;
  veriCulturalAdaptation: string;
  veriRegionalPreference: VeriRegionalLocation;
  veriWorkflowStyle: string;
  veriDataFlowPreferences: string;
  veriStatus: VeriSystemStatus;
}

// Business Workflow
export interface VeriBusinessWorkflow {
  veriWorkflowId: string;
  veriWorkflowName: { vietnamese: string; english: string };
  veriWorkflowType: string;
  veriInvolvedSystems: string[];
  veriExecutionStatus: VeriSystemStatus;
  veriPerformanceScore: number;
}

// Government Connection
export interface VeriGovernmentConnection {
  veriConnectionId: string;
  veriAgencyId: string;
  veriAgencyName: { vietnamese: string; english: string };
  veriConnectionStatus: VeriConnectionStatus;
  veriSecurityLevel: VeriSecurityLevel;
  veriLastSync: Date;
  veriAvailableServices: VeriGovernmentService[];
}

// Government Service
export interface VeriGovernmentService {
  veriServiceId: string;
  veriServiceName: { vietnamese: string; english: string };
  veriServiceType: string;
  veriEnabled: boolean;
  veriStatus: VeriSystemStatus;
}

// Data Flow
export interface VeriDataFlow {
  veriFlowId: string;
  veriSourceSystem: string;
  veriTargetSystem: string;
  veriDirection: 'unidirectional' | 'bidirectional';
  veriDataVolume: string;
  veriLatency: number;
  veriHealth: VeriSystemStatus;
  veriSecurityLevel: VeriSecurityLevel;
  veriFrequency: string;
}

// Cultural Integration
export interface VeriCulturalIntegration {
  veriRegionalLocation: VeriRegionalLocation;
  veriWorkflowStyle: string;
  veriApprovalPatterns: string;
  veriDataFlowPreferences: string;
  veriSystemInteractions: string;
  veriErrorHandling: string;
  veriNotificationPatterns: string;
}

// Orchestration Engine
export interface VeriOrchestrationEngine {
  veriEngineId: string;
  veriOrchestrationMode: string;
  veriActiveWorkflows: number;
  veriOptimizationLevel: number;
  veriAICapabilities: string[];
  veriPerformanceMetrics: VeriPerformanceMetrics;
}

// AI Coordination
export interface VeriAICoordination {
  veriAIEngineId: string;
  veriCoordinationMode: string;
  veriActiveCoordinations: number;
  veriIntelligenceLevel: number;
  veriLearningProgress: number;
  veriOptimizationScore: number;
}

// Integration Health
export interface VeriIntegrationHealth {
  veriOverallScore: number;
  veriHealthTrend: VeriHealthTrend;
  veriActiveIntegrations: number;
  veriIntegrationHealth: VeriSystemStatus;
  veriDataFlowRate: number;
  veriDataFlowHealth: VeriSystemStatus;
  veriConnections: VeriConnectionHealth[];
  veriDataFlows: VeriDataFlow[];
  veriHealthPredictions: VeriHealthPrediction[];
}

// Connection Health
export interface VeriConnectionHealth {
  veriConnectionId: string;
  veriSourceSystem: string;
  veriTargetSystem: string;
  veriHealthStatus: VeriSystemStatus;
  veriLatency: number;
  veriThroughput: number;
  veriErrorRate: number;
}

// Health Prediction
export interface VeriHealthPrediction {
  veriPredictionId: string;
  veriSystemId: string;
  veriPredictedHealth: VeriSystemStatus;
  veriConfidence: number;
  veriTimeframe: string;
  veriRecommendations: string[];
}

// Performance Metrics
export interface VeriPerformanceMetrics {
  veriAverageLatency: number;
  veriThroughput: number;
  veriSuccessRate: number;
  veriErrorRate: number;
  veriUptime: number;
  veriOptimizationGains: number;
}

// Systems Status
export interface VeriSystemsStatus {
  [systemKey: string]: {
    veriStatus: VeriSystemStatus;
    veriUptime: number;
    veriPerformance: number;
    veriIntegrations: number;
    veriLastUpdate: Date;
  };
}

// Ecosystem Metrics
export interface VeriEcosystemMetrics {
  veriTotalSystems: number;
  veriHealthySystems: number;
  veriWarningSystems: number;
  veriCriticalSystems: number;
  veriOfflineSystems: number;
  veriAveragePerformance: number;
  veriTotalIntegrations: number;
  veriDataFlowVolume: string;
}

// Integration Insight
export interface VeriIntegrationInsight {
  veriInsightId: string;
  veriSystemId: string;
  veriInsightType: 'optimization' | 'warning' | 'recommendation' | 'alert';
  veriDescription: { vietnamese: string; english: string };
  veriRecommendedAction: { vietnamese: string; english: string };
  veriPriority: 'high' | 'medium' | 'low';
  veriImpact: string;
}

// MPS Integration
export interface VeriMPSIntegration {
  veriConnectionStatus: VeriConnectionStatus;
  veriDataReporting: boolean;
  veriIncidentNotification: boolean;
  veriComplianceVerification: boolean;
  veriSecurityLevel: VeriSecurityLevel;
  veriLastSync: Date;
  veriConfiguration: VeriMPSConfiguration;
}

// MPS Configuration
export interface VeriMPSConfiguration {
  veriBusinessId: string;
  veriAuthenticationMethod: string;
  veriEncryptionLevel: string;
  veriReportingFrequency: string;
  veriNotificationChannels: string[];
  veriComplianceLevel: string;
}

// Business Context
export interface VeriBusinessContext {
  veriBusinessId: string;
  veriBusinessName: string;
  veriRegionalLocation: VeriRegionalLocation;
  veriIndustry: string;
  veriSize: string;
  veriComplianceRequirements: string[];
}

// Component Props
export interface VeriEcosystemDashboardProps {
  veriSystemsEcosystem: VeriSystemsEcosystem;
  veriLanguage: VeriLanguage;
  veriIntegrationHealth: VeriIntegrationHealth;
  veriOnSystemManage: (systemId: string) => void;
}

export interface VeriGovernmentIntegrationProps {
  veriGovernmentSystems: VeriGovernmentConnection[];
  veriLanguage: VeriLanguage;
  veriBusinessContext: VeriBusinessContext;
  veriOnIntegrationComplete: (connectionId: string) => void;
}

export interface VeriIntegrationContentProps {
  veriIntegrationView: VeriIntegrationView;
  veriLanguage: VeriLanguage;
  veriSystemsEcosystem: VeriSystemsEcosystem;
  veriOrchestrationAI: VeriOrchestrationEngine | undefined;
}
