// VeriPortal_05_BusinessIntelligence - Type Definitions
// Vietnamese Business Intelligence & Analytics System Types

// Core Vietnamese Business Intelligence System
export interface VeriBusinessIntelligenceSystem {
  veriAnalyticsId: string;
  veriBusinessContext: VeriBusinessContext;
  veriAnalyticsScope: VeriAnalyticsScope;
  veriDashboards: VeriDashboard[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriCulturalReporting: VeriCulturalReporting;
  veriAIInsights: VeriAIInsight[];
  veriMarketIntelligence: VeriMarketIntelligence;
  veriComplianceAnalytics: VeriComplianceAnalytics;
}

// Vietnamese Analytics Scope Types
export type VeriAnalyticsScope = 
  | 'compliance-performance'
  | 'market-positioning'
  | 'risk-assessment'
  | 'operational-efficiency'
  | 'competitive-analysis'
  | 'cultural-alignment'
  | 'growth-opportunities'
  | 'regulatory-tracking'
  | 'stakeholder-insights'
  | 'predictive-analytics';

// Vietnamese Business Intelligence Context
export interface VeriBusinessIntelligenceContext {
  veriBusinessProfile: VeriBusinessProfile;
  veriIndustryBenchmarks: VeriIndustryBenchmark[];
  veriMarketPosition: VeriMarketPosition;
  veriComplianceMaturity: VeriComplianceMaturity;
  veriCulturalFactors: VeriCulturalFactor[];
  veriRegionalMarket: VeriRegionalMarket;
  veriCompetitiveEnvironment: VeriCompetitiveEnvironment;
}

// Vietnamese Business Context
export interface VeriBusinessContext {
  veriBusinessId: string;
  veriBusinessName: string;
  veriBusinessNameVi: string;
  veriIndustryType: string;
  veriBusinessSize: 'small' | 'medium' | 'large' | 'enterprise';
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriCulturalPreferences: VeriCulturalPreferences;
  veriComplianceLevel: 'basic' | 'intermediate' | 'advanced' | 'expert';
  veriMarketSegment: string;
  veriBusinessObjectives: string[];
}

// Vietnamese Cultural Preferences
export interface VeriCulturalPreferences {
  veriCommunicationStyle: 'direct' | 'indirect' | 'formal' | 'collaborative';
  veriDecisionMakingStyle: 'hierarchical' | 'consensus' | 'data-driven' | 'relationship-based';
  veriReportingPreferences: 'detailed' | 'summary' | 'visual' | 'narrative';
  veriVisualizationStyle: 'traditional' | 'modern' | 'innovative' | 'minimal';
  veriDataPresentationFormat: 'charts' | 'tables' | 'infographics' | 'mixed';
}

// Vietnamese Business Profile
export interface VeriBusinessProfile {
  veriProfileId: string;
  veriBusinessName: string;
  veriBusinessNameVi: string;
  veriIndustry: string;
  veriSize: string;
  veriRegion: 'north' | 'central' | 'south';
  veriEstablishedYear: number;
  veriEmployeeCount: number;
  veriAnnualRevenue: number;
  veriMarketPosition: string;
  veriComplianceMaturity: string;
  veriDigitalMaturity: string;
  veriCulturalAlignment: VeriCulturalAlignment;
}

// Cultural Alignment
export interface VeriCulturalAlignment {
  veriTraditionalValues: number; // 0-100 score
  veriInnovationOpenness: number; // 0-100 score
  veriHierarchyRespect: number; // 0-100 score
  veriCollaborativeApproach: number; // 0-100 score
  veriRiskTolerance: number; // 0-100 score
  veriChangeAdaptability: number; // 0-100 score
}

// Vietnamese Compliance Analytics
export interface VeriComplianceAnalytics {
  veriComplianceId: string;
  veriOverallScore: number;
  veriComplianceAreas: VeriComplianceArea[];
  veriRiskAnalysis: VeriRiskAnalysis;
  veriPerformanceTrends: VeriPerformanceTrend[];
  veriAuditReadiness: VeriAuditReadiness;
  veriCulturalCompliance: VeriCulturalCompliance;
  veriRecommendations: VeriComplianceRecommendation[];
  veriLastUpdated: Date;
}

// Compliance Area
export interface VeriComplianceArea {
  veriAreaId: string;
  veriAreaName: string;
  veriAreaNameVi: string;
  veriScore: number;
  veriTrend: 'improving' | 'stable' | 'declining';
  veriRiskLevel: 'low' | 'medium' | 'high' | 'critical';
  veriMetrics: VeriComplianceMetric[];
  veriGaps: VeriComplianceGap[];
}

// Compliance Metrics
export interface VeriComplianceMetric {
  veriMetricId: string;
  veriMetricName: string;
  veriMetricNameVi: string;
  veriValue: number;
  veriTarget: number;
  veriTrend: 'up' | 'down' | 'stable';
  veriImportance: 'critical' | 'high' | 'medium' | 'low';
}

// Risk Analysis
export interface VeriRiskAnalysis {
  veriRiskId: string;
  veriOverallRisk: number;
  veriRiskFactors: VeriRiskFactor[];
  veriHistoricalTrends: VeriRiskTrend[];
  veriPredictedRisks: VeriPredictedRisk[];
  veriMitigationStrategies: VeriMitigationStrategy[];
}

// Risk Factor
export interface VeriRiskFactor {
  veriFactorId: string;
  veriFactorName: string;
  veriFactorNameVi: string;
  veriImpact: 'low' | 'medium' | 'high' | 'critical';
  veriProbability: number;
  veriCurrentStatus: string;
  veriMitigationPlan: string;
}

// Vietnamese Market Intelligence
export interface VeriMarketIntelligence {
  veriMarketId: string;
  veriMarketAnalytics: VeriMarketAnalytics;
  veriCompetitivePosition: VeriCompetitivePosition;
  veriMarketOpportunities: VeriMarketOpportunity[];
  veriMarketTrends: VeriMarketTrend[];
  veriCulturalMarketFactors: VeriCulturalMarketFactor[];
  veriStrategicRecommendations: VeriStrategicRecommendation[];
  veriGeneratedAt: Date;
}

// Market Analytics
export interface VeriMarketAnalytics {
  veriMarketSize: string;
  veriGrowthRate: number;
  veriComplianceAdoption: number;
  veriMarketMaturity: string;
  veriIndustryPercentile: number;
  veriCompetitors: VeriCompetitor[];
  veriMarketSegments: VeriMarketSegment[];
}

// Competitive Position
export interface VeriCompetitivePosition {
  veriPositionId: string;
  veriMarketShare: number;
  veriCompetitiveRank: number;
  veriStrengths: string[];
  veriWeaknesses: string[];
  veriOpportunities: string[];
  veriThreats: string[];
  veriDifferentiators: string[];
}

// AI Insights
export interface VeriAIInsight {
  veriInsightId: string;
  veriInsightType: 'performance' | 'recommendation' | 'prediction' | 'opportunity' | 'risk' | 'benchmark';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriConfidence: number;
  veriImpact: 'low' | 'medium' | 'high' | 'critical';
  veriActionable: boolean;
  veriRecommendedActions: string[];
  veriTimeframe: string;
  veriPriority: 'low' | 'medium' | 'high' | 'urgent';
}

// Dashboard Types
export interface VeriDashboard {
  veriDashboardId: string;
  veriDashboardType: VeriAnalyticsScope;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriWidgets: VeriWidget[];
  veriRefreshInterval: number;
  veriLastUpdated: Date;
}

// Widget Types
export interface VeriWidget {
  veriWidgetId: string;
  veriWidgetType: 'chart' | 'metric' | 'table' | 'gauge' | 'trend' | 'insight';
  veriTitle: string;
  veriTitleVi: string;
  veriData: any;
  veriConfiguration: VeriWidgetConfiguration;
  veriPosition: VeriWidgetPosition;
}

// Widget Configuration
export interface VeriWidgetConfiguration {
  veriChartType?: 'line' | 'bar' | 'pie' | 'area' | 'scatter' | 'gauge' | 'heatmap';
  veriColorScheme: string[];
  veriDataFormat: string;
  veriInteractive: boolean;
  veriExportable: boolean;
  veriCulturalFormatting: boolean;
}

// Widget Position
export interface VeriWidgetPosition {
  veriRow: number;
  veriColumn: number;
  veriWidth: number;
  veriHeight: number;
}

// Cultural Reporting
export interface VeriCulturalReporting {
  veriReportingStyle: 'executive' | 'detailed' | 'visual' | 'narrative';
  veriCommunicationTone: 'formal' | 'professional' | 'friendly' | 'direct';
  veriCulturalContext: 'traditional' | 'modern' | 'international' | 'local';
  veriLanguagePreference: 'vietnamese' | 'english' | 'bilingual';
  veriVisualizationPreferences: VeriVisualizationPreferences;
}

// Visualization Preferences
export interface VeriVisualizationPreferences {
  veriColorPalette: 'traditional' | 'modern' | 'business' | 'vibrant';
  veriChartStyle: 'clean' | 'detailed' | 'artistic' | 'technical';
  veriDataDensity: 'minimal' | 'balanced' | 'comprehensive' | 'detailed';
  veriInteractivityLevel: 'basic' | 'moderate' | 'advanced' | 'expert';
}

// Performance Trends
export interface VeriPerformanceTrend {
  veriTrendId: string;
  veriMetricName: string;
  veriTimeRange: string;
  veriDataPoints: VeriDataPoint[];
  veriTrendDirection: 'upward' | 'downward' | 'stable' | 'volatile';
  veriSeasonality: boolean;
  veriPrediction: VeriTrendPrediction;
}

// Data Point
export interface VeriDataPoint {
  veriTimestamp: Date;
  veriValue: number;
  veriContext?: string;
}

// Trend Prediction
export interface VeriTrendPrediction {
  veriPredictedValues: VeriDataPoint[];
  veriConfidenceInterval: number;
  veriAccuracy: number;
  veriFactors: string[];
}

// Strategic Recommendations
export interface VeriStrategicRecommendation {
  veriRecommendationId: string;
  veriType: 'strategic' | 'operational' | 'tactical' | 'cultural';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriPriority: 'low' | 'medium' | 'high' | 'critical';
  veriImpact: 'low' | 'medium' | 'high' | 'transformational';
  veriTimeframe: 'immediate' | 'short-term' | 'medium-term' | 'long-term';
  veriImplementationSteps: string[];
  veriExpectedOutcomes: string[];
  veriRiskFactors: string[];
  veriResourceRequirements: VeriResourceRequirement[];
}

// Resource Requirements
export interface VeriResourceRequirement {
  veriResourceType: 'human' | 'financial' | 'technological' | 'time';
  veriDescription: string;
  veriQuantity: number;
  veriUnit: string;
  veriCritical: boolean;
}

// Market Opportunity
export interface VeriMarketOpportunity {
  veriOpportunityId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriMarketSize: number;
  veriPotentialRevenue: number;
  veriCompetitiveIntensity: 'low' | 'medium' | 'high';
  veriTimeToEntry: number; // months
  veriRequiredInvestment: number;
  veriRiskLevel: 'low' | 'medium' | 'high';
  veriCulturalAlignment: number; // 0-100 score
  veriStrategicFit: number; // 0-100 score
}

// Market Trend
export interface VeriMarketTrend {
  veriTrendId: string;
  veriTrendName: string;
  veriTrendNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriImpact: 'disruptive' | 'transformative' | 'incremental' | 'minimal';
  veriTimeframe: 'current' | 'emerging' | 'future' | 'long-term';
  veriProbability: number; // 0-100
  veriBusinessImplication: string;
  veriRecommendedResponse: string;
}

// Analytics Props Interfaces
export interface VeriBusinessIntelligenceProps {
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriInitialScope?: VeriAnalyticsScope;
  veriOnAnalyticsUpdate?: (analytics: VeriBusinessIntelligenceSystem) => void;
  veriOnInsightAction?: (insight: VeriAIInsight) => void;
  veriOnRecommendationAction?: (recommendation: VeriStrategicRecommendation) => void;
}

export interface VeriComplianceAnalyticsProps {
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriAIAnalytics?: any;
  veriOnInsightAction?: (insight: VeriAIInsight) => void;
}

export interface VeriMarketIntelligenceProps {
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriMarketData?: any;
  veriOnStrategyRecommendation?: (recommendation: VeriStrategicRecommendation) => void;
}

// Additional Supporting Interfaces
export interface VeriIndustryBenchmark {
  veriIndustry: string;
  veriMetric: string;
  veriAverageValue: number;
  veriTopPerformers: number;
  veriYourPosition: number;
  veriRanking: number;
}

export interface VeriMarketPosition {
  veriMarketShare: number;
  veriCompetitiveRank: number;
  veriGrowthRate: number;
  veriMarketPresence: 'emerging' | 'established' | 'leading' | 'dominant';
}

export interface VeriComplianceMaturity {
  veriMaturityLevel: 'initial' | 'developing' | 'defined' | 'managed' | 'optimized';
  veriScore: number;
  veriAreas: VeriComplianceArea[];
  veriNextLevel: string;
}

export interface VeriCulturalFactor {
  veriFactorId: string;
  veriFactorName: string;
  veriFactorNameVi: string;
  veriInfluence: 'high' | 'medium' | 'low';
  veriDescription: string;
  veriBusinessImpact: string;
}

export interface VeriRegionalMarket {
  veriRegion: 'north' | 'central' | 'south';
  veriMarketSize: number;
  veriGrowthRate: number;
  veriCompetitiveIntensity: string;
  veriCulturalCharacteristics: string[];
  veriBusinessOpportunities: string[];
}

export interface VeriCompetitiveEnvironment {
  veriCompetitors: VeriCompetitor[];
  veriMarketLeader: string;
  veriCompetitiveIntensity: 'low' | 'medium' | 'high' | 'fierce';
  veriDifferentiationOpportunities: string[];
  veriCompetitiveThreats: string[];
}

export interface VeriCompetitor {
  veriCompetitorId: string;
  veriName: string;
  veriMarketShare: number;
  veriStrengths: string[];
  veriWeaknesses: string[];
  veriStrategy: string;
  veriCompetitiveThreat: 'low' | 'medium' | 'high';
}

export interface VeriMarketSegment {
  veriSegmentId: string;
  veriSegmentName: string;
  veriSize: number;
  veriGrowthRate: number;
  veriProfitability: 'low' | 'medium' | 'high';
  veriAccessibility: 'easy' | 'moderate' | 'difficult';
}

export interface VeriComplianceGap {
  veriGapId: string;
  veriGapName: string;
  veriGapNameVi: string;
  veriSeverity: 'low' | 'medium' | 'high' | 'critical';
  veriDescription: string;
  veriRemediationSteps: string[];
  veriTimeframe: string;
}

export interface VeriRiskTrend {
  veriDate: Date;
  veriRiskScore: number;
  veriRiskFactors: string[];
  veriMitigationEffectiveness: number;
}

export interface VeriPredictedRisk {
  veriRiskType: string;
  veriProbability: number;
  veriImpact: 'low' | 'medium' | 'high' | 'critical';
  veriTimeframe: string;
  veriEarlyWarnings: string[];
}

export interface VeriMitigationStrategy {
  veriStrategyId: string;
  veriStrategyName: string;
  veriDescription: string;
  veriEffectiveness: number;
  veriImplementationCost: number;
  veriTimeToImplement: number;
}

export interface VeriAuditReadiness {
  veriReadinessScore: number;
  veriReadyAreas: string[];
  veriImprovementNeeded: VeriComplianceGap[];
  veriEstimatedPreparationTime: number;
  veriRecommendedActions: string[];
}

export interface VeriCulturalCompliance {
  veriCulturalAlignment: number;
  veriAdaptationNeeds: string[];
  veriCulturalStrengths: string[];
  veriCulturalChallenges: string[];
  veriRecommendedApproach: string;
}

export interface VeriComplianceRecommendation {
  veriRecommendationId: string;
  veriType: 'immediate' | 'short-term' | 'long-term' | 'strategic';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriImpact: 'low' | 'medium' | 'high' | 'critical';
  veriEffort: 'low' | 'medium' | 'high';
  veriPriority: number;
}

export interface VeriCulturalMarketFactor {
  veriFactorName: string;
  veriFactorNameVi: string;
  veriInfluence: 'positive' | 'negative' | 'neutral';
  veriImpact: 'low' | 'medium' | 'high';
  veriDescription: string;
  veriBusinessImplication: string;
}

// Export all types
export type * from './types';