// VeriPortal_02_ComplianceWizards TypeScript Types
// Vietnamese PDPL 2025 Compliance Wizards System Types

// Core Vietnamese Compliance Wizards Engine
export interface VeriComplianceWizardSystem {
  veriWizardId: string;
  veriWizardType: VeriWizardType;
  veriBusinessContext: VeriBusinessContext;
  veriComplianceSteps: VeriComplianceStep[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriCulturalAdaptations: VeriCulturalAdaptations;
  veriProgressState: VeriWizardProgress;
  veriAIRecommendations: VeriAIRecommendation[];
  veriComplianceScore: VeriComplianceScore;
}

// Vietnamese Compliance Wizard Types
export type VeriWizardType = 
  | 'pdpl-2025-setup'
  | 'mps-integration'
  | 'cultural-compliance'
  | 'risk-management'
  | 'data-mapping'
  | 'policy-generation'
  | 'audit-preparation'
  | 'cross-border-transfer';

// Vietnamese Business Context for Compliance
export interface VeriBusinessContext {
  veriBusinessId: string;
  veriIndustryType: VeriIndustryType;
  veriDataProcessingLevel: 'basic' | 'moderate' | 'complex' | 'enterprise';
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriComplianceMaturity: 'beginner' | 'intermediate' | 'advanced';
  veriRegulatoryHistory: VeriRegulatoryHistory;
  veriStakeholderRoles: VeriStakeholderRole[];
  veriCulturalPreferences: VeriCulturalPreferences;
}

export interface VeriIndustryType {
  veriIndustryCode: string;
  veriIndustryName: string;
  veriIndustryNameVi: string;
  veriRegulatoryLevel: 'low' | 'medium' | 'high' | 'critical';
  veriSpecialRequirements: string[];
}

export interface VeriRegulatoryHistory {
  veriPreviousCompliance: boolean;
  veriComplianceFrameworks: string[];
  veriAuditHistory: VeriAuditRecord[];
  veriIncidentHistory: VeriIncidentRecord[];
}

export interface VeriStakeholderRole {
  veriRoleId: string;
  veriRoleName: string;
  veriRoleNameVi: string;
  veriResponsibilities: string[];
  veriAccessLevel: 'basic' | 'elevated' | 'admin';
}

export interface VeriCulturalPreferences {
  veriCommunicationStyle: 'formal' | 'consultative' | 'collaborative' | 'direct';
  veriDecisionMakingStyle: 'hierarchical' | 'consensus' | 'collaborative' | 'agile';
  veriInformationDensity: 'minimal' | 'moderate' | 'comprehensive' | 'detailed';
  veriValidationLevel: 'essential' | 'standard' | 'thorough' | 'rigorous';
}

// Compliance Steps and Progress
export interface VeriComplianceStep {
  veriStepId: string;
  veriStepKey: string;
  veriStepName: string;
  veriStepNameVi: string;
  veriStepDescription: string;
  veriStepDescriptionVi: string;
  veriStepOrder: number;
  veriIsRequired: boolean;
  veriIsCultural: boolean;
  veriEstimatedTime: number; // minutes
  veriComplexityLevel: 'basic' | 'intermediate' | 'advanced' | 'expert';
  veriPrerequisites: string[];
  veriValidationRules: VeriValidationRule[];
}

export interface VeriWizardProgress {
  veriCurrentStep: string;
  veriCompletedSteps: string[];
  veriStepData: Record<string, any>;
  veriOverallProgress: number; // percentage
  veriComplianceScore: number;
  veriEstimatedTimeRemaining: number;
  veriStartedAt: Date;
  veriLastUpdated: Date;
}

// Cultural Adaptations
export interface VeriCulturalAdaptations {
  veriRegionalAdaptation: VeriRegionalAdaptation;
  veriBusinessTypeAdaptation: VeriBusinessTypeAdaptation;
  veriLanguageAdaptations: VeriLanguageAdaptations;
  veriUIAdaptations: VeriUIAdaptations;
  veriWorkflowAdaptations: VeriWorkflowAdaptations;
}

export interface VeriRegionalAdaptation {
  veriRegion: 'north' | 'central' | 'south';
  veriRegionName: string;
  veriWizardPacing: string;
  veriInformationDensity: string;
  veriValidationLevel: string;
  veriCommunicationStyle: string;
  veriDecisionSupport: string;
  veriWizardPersonality: string;
}

export interface VeriBusinessTypeAdaptation {
  veriBusinessType: 'sme' | 'startup' | 'enterprise' | 'government';
  veriComplexityLevel: string;
  veriTimeInvestment: string;
  veriSupportLevel: string;
  veriDocumentationStyle: string;
  veriTerminology: string;
  veriExamples: string;
  veriValidation: string;
}

export interface VeriLanguageAdaptations {
  veriPrimaryLanguage: 'vietnamese' | 'english';
  veriSecondaryLanguage: 'vietnamese' | 'english';
  veriTerminologyStyle: 'business' | 'technical' | 'legal' | 'friendly';
  veriCulturalTerms: Record<string, string>;
  veriRegionalDialects: Record<string, string>;
}

export interface VeriUIAdaptations {
  veriColorScheme: string;
  veriTypography: string;
  veriSpacing: string;
  veriAnimations: string;
  veriIcons: string;
  veriLayout: string;
}

export interface VeriWorkflowAdaptations {
  veriStepSequencing: string;
  veriValidationFrequency: string;
  veriHelpSystem: string;
  veriProgressDisplay: string;
  veriDecisionPoints: string;
}

// AI Recommendations and Analysis
export interface VeriAIRecommendation {
  veriRecommendationId: string;
  veriRecommendationType: 'legal-basis' | 'data-mapping' | 'security' | 'policy' | 'cultural';
  veriPriorityLevel: 'low' | 'medium' | 'high' | 'critical';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriReasoning: string;
  veriReasoningVi: string;
  veriBusinessMatch: number; // percentage
  veriCulturalFit: number; // percentage
  veriImplementationComplexity: 'low' | 'medium' | 'high' | 'very-high';
  veriAIConfidence: number; // percentage
  veriSupportingData: Record<string, any>;
}

export interface VeriComplianceScore {
  veriOverallScore: number;
  veriCategoryScores: Record<string, number>;
  veriRiskAssessment: VeriRiskAssessment;
  veriImprovementRecommendations: VeriImprovementRecommendation[];
  veriConfidenceLevel: number;
  veriLastCalculated: Date;
  veriTrendData: VeriScoreTrend[];
}

export interface VeriRiskAssessment {
  veriOverallRisk: 'low' | 'medium' | 'high' | 'critical';
  veriRiskFactors: VeriRiskFactor[];
  veriMitigationRecommendations: VeriMitigationRecommendation[];
}

export interface VeriRiskFactor {
  veriFactorId: string;
  veriFactorName: string;
  veriFactorNameVi: string;
  veriRiskLevel: 'low' | 'medium' | 'high' | 'critical';
  veriDescription: string;
  veriDescriptionVi: string;
  veriImpact: string;
  veriLikelihood: string;
}

export interface VeriMitigationRecommendation {
  veriRecommendationId: string;
  veriRiskFactorId: string;
  veriMitigationAction: string;
  veriMitigationActionVi: string;
  veriPriority: 'low' | 'medium' | 'high' | 'critical';
  veriEffortLevel: 'minimal' | 'moderate' | 'significant' | 'extensive';
  veriTimeframe: string;
  veriResources: string[];
}

export interface VeriImprovementRecommendation {
  veriRecommendationId: string;
  veriCategory: string;
  veriCurrentScore: number;
  veriTargetScore: number;
  veriImprovement: string;
  veriImprovementVi: string;
  veriActionItems: string[];
  veriPriority: 'low' | 'medium' | 'high' | 'critical';
}

export interface VeriScoreTrend {
  veriDate: Date;
  veriScore: number;
  veriCategory?: string;
  veriChange: number;
}

// Legal Basis Setup Types
export interface VeriLegalBasisData {
  veriSelectedBases: string[];
  veriProcessingPurposes: Record<string, string[]>;
  veriDataCategories: Record<string, VeriDataCategory[]>;
  veriRetentionPeriods: Record<string, VeriRetentionPeriod>;
  veriLegalDocuments: VeriLegalDocument[];
}

export interface VeriDataCategory {
  veriCategoryId: string;
  veriCategoryName: string;
  veriCategoryNameVi: string;
  veriDataTypes: string[];
  veriSensitivityLevel: 'basic' | 'personal' | 'sensitive' | 'special';
  veriProcessingBasis: string;
  veriStorageLocation: string;
}

export interface VeriRetentionPeriod {
  veriPeriodId: string;
  veriDuration: number; // months
  veriJustification: string;
  veriJustificationVi: string;
  veriAutoDeletion: boolean;
  veriArchivalPolicy: string;
}

export interface VeriLegalDocument {
  veriDocumentId: string;
  veriDocumentType: string;
  veriDocumentName: string;
  veriDocumentNameVi: string;
  veriVersion: string;
  veriContent: string;
  veriApprovalStatus: 'draft' | 'review' | 'approved' | 'published';
  veriLastUpdated: Date;
}

// Legal Basis Recommendations
export interface VeriLegalBasisRecommendation {
  veriLegalBasisName: string;
  veriVietnameseReason: string;
  veriBusinessMatch: number;
  veriPriorityLevel: 'low' | 'medium' | 'high' | 'critical';
  veriAIConfidence: number;
  veriRegulatoryAlignment: number;
  veriImplementationComplexity: 'low' | 'medium' | 'high' | 'very-high';
  veriCulturalAppropriateness: number;
  veriSupportingData: Record<string, any>;
}

// Validation Rules and Results
export interface VeriValidationRule {
  veriRuleId: string;
  veriRuleName: string;
  veriRuleType: 'required' | 'conditional' | 'cultural' | 'regulatory';
  veriValidationFunction: string;
  veriErrorMessage: string;
  veriErrorMessageVi: string;
  veriSeverity: 'info' | 'warning' | 'error' | 'critical';
}

export interface VeriValidationResult {
  veriIsValid: boolean;
  veriErrors: VeriValidationError[];
  veriWarnings: VeriValidationWarning[];
  veriSuggestions: VeriValidationSuggestion[];
}

export interface VeriValidationError {
  veriErrorId: string;
  veriRuleId: string;
  veriMessage: string;
  veriMessageVi: string;
  veriSeverity: 'error' | 'critical';
  veriFieldPath: string;
  veriSuggestedFix: string;
}

export interface VeriValidationWarning {
  veriWarningId: string;
  veriRuleId: string;
  veriMessage: string;
  veriMessageVi: string;
  veriRecommendation: string;
  veriRecommendationVi: string;
}

export interface VeriValidationSuggestion {
  veriSuggestionId: string;
  veriMessage: string;
  veriMessageVi: string;
  veriImprovement: string;
  veriBenefit: string;
}

// AI Engine Types
export interface VeriAIWizardEngine {
  veriEngineId: string;
  veriEngineVersion: string;
  veriCapabilities: string[];
  veriLanguages: string[];
  veriCulturalModels: string[];
  veriAnalysisTypes: string[];
}

export interface VeriAIComplianceAnalysis {
  veriAnalysisId: string;
  veriBusinessContext: VeriBusinessContext;
  veriComplianceRequirements: VeriComplianceRequirement[];
  veriRiskFactors: VeriRiskFactor[];
  veriRecommendations: VeriAIRecommendation[];
  veriConfidenceScore: number;
  veriAnalysisDate: Date;
  veriDataMappingRecommendations?: VeriDataMappingRecommendation[];
}

export interface VeriComplianceRequirement {
  veriRequirementId: string;
  veriRequirementType: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriMandatory: boolean;
  veriDeadline?: Date;
  veriComplexity: 'low' | 'medium' | 'high' | 'very-high';
  veriEstimatedEffort: number; // hours
}

export interface VeriDataMappingRecommendation {
  veriRecommendationId: string;
  veriDataFlow: string;
  veriSource: string;
  veriDestination: string;
  veriProcessingPurpose: string;
  veriLegalBasis: string;
  veriRetentionPeriod: string;
  veriSecurityMeasures: string[];
  veriPriority: 'low' | 'medium' | 'high' | 'critical';
}

// Audit and Incident Records
export interface VeriAuditRecord {
  veriAuditId: string;
  veriAuditDate: Date;
  veriAuditType: string;
  veriAuditScope: string;
  veriFindings: VeriAuditFinding[];
  veriScore: number;
  veriStatus: 'completed' | 'in-progress' | 'planned';
}

export interface VeriAuditFinding {
  veriFindingId: string;
  veriCategory: string;
  veriSeverity: 'low' | 'medium' | 'high' | 'critical';
  veriDescription: string;
  veriDescriptionVi: string;
  veriRecommendation: string;
  veriRecommendationVi: string;
  veriStatus: 'open' | 'in-progress' | 'resolved';
}

export interface VeriIncidentRecord {
  veriIncidentId: string;
  veriIncidentDate: Date;
  veriIncidentType: string;
  veriSeverity: 'low' | 'medium' | 'high' | 'critical';
  veriDescription: string;
  veriDescriptionVi: string;
  veriImpact: string;
  veriResolution: string;
  veriStatus: 'reported' | 'investigating' | 'resolved' | 'closed';
  veriLessonsLearned: string;
}

// Component Props Types
export interface VeriComplianceWizardProps {
  veriBusinessContext?: VeriBusinessContext;
  veriLanguage?: 'vietnamese' | 'english';
  veriOnComplete?: (result: VeriComplianceWizardResult) => void;
  veriOnStepChange?: (step: string) => void;
  veriCulturalStyle?: string;
}

export interface VeriPDPLWizardProps {
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriOnComplete: (result: VeriPDPLWizardResult) => void;
}

export interface VeriLegalBasisProps {
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriAIAnalysis?: VeriAIComplianceAnalysis;
  veriOnComplete: (data: VeriLegalBasisData) => void;
}

export interface VeriWizardStepProps {
  veriStepKey: string;
  veriBusinessContext: VeriBusinessContext;
  veriLanguage: 'vietnamese' | 'english';
  veriStepData?: any;
  veriAIRecommendations?: VeriAIRecommendation[];
  veriOnComplete: (data: any) => void;
  veriOnValidation?: (isValid: boolean) => void;
}

// Result Types
export interface VeriComplianceWizardResult {
  veriWizardType: VeriWizardType;
  veriCompletedSteps: string[];
  veriStepData: Record<string, any>;
  veriComplianceScore: VeriComplianceScore;
  veriGeneratedDocuments: VeriLegalDocument[];
  veriRecommendations: VeriAIRecommendation[];
  veriCompletedAt: Date;
}

export interface VeriPDPLWizardResult {
  veriLegalBasisData: VeriLegalBasisData;
  veriDataMappingData: any;
  veriConsentManagementData: any;
  veriPrivacyNoticeData: any;
  veriSecurityMeasuresData: any;
  veriIncidentResponseData: any;
  veriDPOSetupData: any;
  veriAuditPreparationData: any;
  veriComplianceScore: VeriComplianceScore;
}

// Context Types
export interface VeriWizardContextType {
  veriWizardState: VeriComplianceWizardSystem | null;
  veriSetWizardState: (state: VeriComplianceWizardSystem) => void;
  veriCurrentWizard: VeriWizardType;
  veriSetCurrentWizard: (wizard: VeriWizardType) => void;
  veriLanguage: 'vietnamese' | 'english';
  veriSetLanguage: (language: 'vietnamese' | 'english') => void;
  veriBusinessContext: VeriBusinessContext | null;
  veriSetBusinessContext: (context: VeriBusinessContext) => void;
  veriAIEngine: VeriAIWizardEngine | null;
  veriSetAIEngine: (engine: VeriAIWizardEngine) => void;
}

// Mobile Types
export interface VeriMobileWizardProps {
  veriIsMobile?: boolean;
  veriTouchOptimized?: boolean;
  veriSwipeNavigation?: boolean;
  veriFloatingActionBar?: boolean;
  veriQuickActions?: string[];
}

// PDPL Step Types
export type VeriPDPLStep = 
  | 'legal-basis-setup'
  | 'data-mapping'
  | 'consent-management'
  | 'privacy-notice'
  | 'security-measures'
  | 'incident-response'
  | 'dpo-setup'
  | 'audit-preparation';

// Additional Types for AI Services
export interface VeriWizardData {
  legalBasis?: VeriLegalBasisData;
  dataMapping?: any;
  security?: any;
  policies?: any;
  [key: string]: any;
}