// VeriPortal_03_DocumentGeneration - Vietnamese Legal Document Generation System
// Advanced AI-Powered Document Generation with Vietnamese Cultural Intelligence

export interface VeriDocumentGenerationSystem {
  veriDocumentId: string;
  veriDocumentType: VeriDocumentType;
  veriBusinessContext: VeriBusinessProfile;
  veriLegalRequirements: VeriLegalRequirement[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
  veriGenerationStatus: VeriDocumentGenerationStatus;
  veriAIPersonalization: VeriAIPersonalization;
  veriLegalValidation: VeriLegalValidation;
}

// Vietnamese Legal Document Types
export type VeriDocumentType = 
  | 'privacy-policy'
  | 'privacy-notice'
  | 'consent-forms'
  | 'data-processing-agreement'
  | 'data-subject-rights-procedure'
  | 'security-incident-response-plan'
  | 'data-retention-policy'
  | 'cross-border-transfer-agreement'
  | 'dpo-appointment-letter'
  | 'compliance-audit-checklist'
  | 'employee-privacy-training-materials'
  | 'vendor-privacy-assessment';

// Vietnamese Legal Document Context
export interface VeriLegalDocumentContext {
  veriBusinessProfile: VeriBusinessProfile;
  veriIndustryRegulations: VeriIndustryRegulation[];
  veriDataProcessingActivities: VeriDataProcessingActivity[];
  veriLegalBases: VeriLegalBasis[];
  veriStakeholderRoles: VeriStakeholderRole[];
  veriRegionalCompliance: VeriRegionalCompliance;
  veriCulturalBusinessStyle: VeriCulturalBusinessStyle;
}

export interface VeriBusinessProfile {
  veriCompanyName: string;
  veriIndustryType: string;
  veriBusinessSize: 'startup' | 'sme' | 'enterprise';
  veriEmployeeCount: number;
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriDataProcessingVolume: 'low' | 'medium' | 'high';
  veriCommunicationStyle: 'formal' | 'modern' | 'casual';
  veriStakeholderTypes: string[];
}

export interface VeriIndustryRegulation {
  veriRegulationId: string;
  veriRegulationType: string;
  veriApplicableDocuments: VeriDocumentType[];
  veriRequirements: string[];
  veriComplianceLevel: 'mandatory' | 'recommended' | 'optional';
}

export interface VeriDataProcessingActivity {
  veriActivityId: string;
  veriActivityName: string;
  veriDataCategories: string[];
  veriProcessingPurposes: string[];
  veriLegalBasis: VeriLegalBasis;
  veriDataRetentionPeriod: string;
  veriSecurityMeasures: string[];
}

export interface VeriLegalBasis {
  veriBasisType: 'consent' | 'contract' | 'legal_obligation' | 'vital_interests' | 'public_task' | 'legitimate_interests';
  veriBasisDescription: string;
  veriApplicableActivities: string[];
  veriConsentRequirements?: VeriConsentRequirements;
}

export interface VeriConsentRequirements {
  veriConsentType: 'explicit' | 'implicit';
  veriWithdrawalMechanism: string;
  veriConsentRecords: boolean;
  veriMinorConsent: boolean;
}

export interface VeriStakeholderRole {
  veriRoleId: string;
  veriRoleName: string;
  veriResponsibilities: string[];
  veriDataAccessLevel: 'full' | 'limited' | 'restricted';
  veriTrainingRequired: boolean;
}

export interface VeriRegionalCompliance {
  veriRegion: 'north' | 'central' | 'south';
  veriSpecificRequirements: string[];
  veriCulturalConsiderations: string[];
  veriLanguageAdaptations: string[];
}

export interface VeriCulturalBusinessStyle {
  veriFormalityLevel: 'high' | 'moderate' | 'low';
  veriCommunicationStyle: 'hierarchical' | 'collaborative' | 'direct';
  veriDocumentStructure: 'traditional' | 'modern' | 'innovative';
  veriLanguageComplexity: 'comprehensive' | 'balanced' | 'simplified';
}

export interface VeriCulturalDocumentAdaptations {
  veriHeaderStyle: string;
  veriGreeting: string;
  veriClosing: string;
  veriSignature: string;
  veriFormality: 'high' | 'moderate' | 'friendly';
  veriLanguageComplexity: 'comprehensive' | 'balanced' | 'simplified';
  veriRegionalAdaptations: VeriRegionalAdaptations;
}

export interface VeriRegionalAdaptations {
  veriLanguageStyle: string;
  veriTerminology: string;
  veriStructure: string;
  veriTone: string;
}

export interface VeriDocumentGenerationStatus {
  veriStatus: 'pending' | 'analyzing' | 'generating' | 'validating' | 'completed' | 'error';
  veriProgress: number;
  veriCurrentStep: string;
  veriEstimatedTimeRemaining?: number;
  veriGeneratedSections?: string[];
  veriValidationResults?: VeriValidationResult[];
}

export interface VeriValidationResult {
  veriSection: string;
  veriValidationType: 'legal' | 'cultural' | 'language' | 'compliance';
  veriStatus: 'pass' | 'warning' | 'fail';
  veriMessage: string;
  veriSuggestions?: string[];
}

export interface VeriAIPersonalization {
  veriPersonalizationScore: number;
  veriBusinessAnalysis: VeriBusinessAnalysis;
  veriCulturalProfile: VeriCulturalProfile;
  veriIndustrySpecificContent: VeriIndustryContent[];
  veriAIConfidenceScore: number;
  veriRecommendedSections: string[];
}

export interface VeriBusinessAnalysis {
  veriComplexityLevel: 'low' | 'medium' | 'high';
  veriIndustrySpecificRequirements: string[];
  veriDataProcessingRisk: 'low' | 'medium' | 'high';
  veriRegulatoryComplexity: 'simple' | 'moderate' | 'complex';
  veriStakeholderComplexity: 'basic' | 'moderate' | 'advanced';
}

export interface VeriCulturalProfile {
  veriRegionalPreferences: VeriRegionalPreferences;
  veriBusinessCultureType: string;
  veriCommunicationPreferences: VeriCommunicationPreferences;
  veriLegalLanguageStyle: string;
}

export interface VeriRegionalPreferences {
  veriLanguageVariation: string;
  veriFormality: string;
  veriBusinessEtiquette: string[];
  veriDocumentExpectations: string[];
}

export interface VeriCommunicationPreferences {
  veriPreferredTone: string;
  veriDetailLevel: string;
  veriExampleUsage: string;
  veriExplanationStyle: string;
}

export interface VeriIndustryContent {
  veriIndustryId: string;
  veriSpecificTerminology: string[];
  veriRegulatoryReferences: string[];
  veriCommonPractices: string[];
  veriRiskFactors: string[];
}

export interface VeriLegalValidation {
  veriPDPLCompliance: VeriComplianceResult;
  veriMPSCompliance: VeriComplianceResult;
  veriLanguageCompliance: VeriComplianceResult;
  veriIndustryCompliance: VeriComplianceResult;
  veriCulturalCompliance: VeriComplianceResult;
  veriOverallComplianceScore: number;
  veriValidationIssues: VeriValidationIssue[];
  veriImprovementRecommendations: VeriImprovementRecommendation[];
}

export interface VeriComplianceResult {
  veriScore: number;
  veriStatus: 'compliant' | 'partially_compliant' | 'non_compliant';
  veriRequirementsMet: string[];
  veriRequirementsMissing: string[];
  veriRecommendations: string[];
}

export interface VeriValidationIssue {
  veriIssueId: string;
  veriIssueType: 'critical' | 'warning' | 'suggestion';
  veriSection: string;
  veriDescription: string;
  veriImpact: string;
  veriResolution: string;
}

export interface VeriImprovementRecommendation {
  veriRecommendationId: string;
  veriPriority: 'high' | 'medium' | 'low';
  veriCategory: string;
  veriDescription: string;
  veriImplementationSteps: string[];
  veriExpectedImprovement: string;
}

// Document Generation Props
export interface VeriDocumentGenerationProps {
  veriBusinessContext?: VeriBusinessProfile;
  veriLanguage?: 'vietnamese' | 'english';
  veriOnComplete?: (result: VeriGeneratedDocument) => void;
  veriOnStepChange?: (step: string) => void;
  veriCulturalStyle?: string;
  veriSelectedDocuments?: VeriDocumentType[];
}

export interface VeriGeneratedDocument {
  veriDocumentId: string;
  veriDocumentType: VeriDocumentType;
  veriDocumentContent: VeriDocumentContent;
  veriBusinessAnalysis: VeriBusinessAnalysis;
  veriLegalValidation: VeriLegalValidation;
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
  veriAIPersonalizationScore: number;
  veriGeneratedAt: Date;
  veriFileFormat: 'html' | 'pdf' | 'docx';
  veriDownloadUrl?: string;
}

export interface VeriDocumentContent {
  veriSections: VeriDocumentSection[];
  veriDocumentMetadata: VeriDocumentMetadata;
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
  veriLegalComplianceLevel: number;
  veriAIGenerationQuality: number;
}

export interface VeriDocumentSection {
  veriSectionId: string;
  veriSectionTitle: string;
  veriSectionContent: string;
  veriSectionType: 'header' | 'body' | 'list' | 'table' | 'footer';
  veriLegalReferences: string[];
  veriCulturalNotes: string[];
}

export interface VeriDocumentMetadata {
  veriTitle: string;
  veriVersion: string;
  veriCreatedBy: string;
  veriCreatedAt: Date;
  veriLastModified: Date;
  veriLanguage: 'vietnamese' | 'english';
  veriDocumentPurpose: string;
  veriApplicableRegulations: string[];
}

// Privacy Policy Specific Types
export interface VeriPrivacyPolicyProps {
  veriBusinessContext: VeriBusinessProfile;
  veriLanguage: 'vietnamese' | 'english';
  veriLegalRequirements: VeriLegalRequirement[];
  veriOnGenerate: (policy: VeriGeneratedDocument) => void;
}

export interface VeriLegalRequirement {
  veriRequirementId: string;
  veriRequirementType: string;
  veriDescription: string;
  veriMandatory: boolean;
  veriApplicableDocuments: VeriDocumentType[];
}

export interface VeriPolicyConfiguration {
  veriIncludedSections: string[];
  veriCommunicationStyle: 'formal' | 'modern' | 'casual';
  veriLegalComplexity: 'simple' | 'moderate' | 'comprehensive';
  veriIndustrySpecific: boolean;
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
}

export interface VeriAIDocumentAnalysis {
  veriIndustrySpecificRequirements: string;
  veriComplexityLevel: 'low' | 'medium' | 'high';
  veriCulturalStyle: string;
  veriLegalRequirements: VeriLegalRequirement[];
  veriSectionRecommendations: Record<string, string[]>;
  veriPersonalizationScore: number;
  veriAIConfidence: number;
}

export interface VeriGenerationProgress {
  veriInProgress: boolean;
  veriProgressPercentage: number;
  veriCurrentStep: string;
  veriEstimatedTimeRemaining: number;
  veriCompletedSteps: string[];
}

// Template Types
export interface VeriDocumentTemplate {
  veriTemplateId: string;
  veriTitle: Record<'vietnamese' | 'english', string>;
  veriDescription: Record<'vietnamese' | 'english', string>;
  veriDocumentType: VeriDocumentType;
  veriSections: VeriTemplateSection[];
  veriFeatures: string[];
  veriAICompatibility: number;
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
  veriIndustrySpecific: string[];
}

export interface VeriTemplateSection {
  veriSectionId: string;
  veriSectionTitle: Record<'vietnamese' | 'english', string>;
  veriSectionContent: string;
  veriIsRequired: boolean;
  veriCustomizable: boolean;
  veriAIGenerated: boolean;
}

export interface VeriTemplateCustomization {
  veriTemplateId: string;
  veriCustomizedSections: Record<string, string>;
  veriBusinessSpecificContent: string[];
  veriCulturalAdaptations: VeriCulturalDocumentAdaptations;
  veriLegalPersonalization: string[];
}

// Context Provider Types
export interface VeriDocumentContextType {
  veriDocumentState: VeriDocumentGenerationSystem | null;
  veriSetDocumentState: (state: VeriDocumentGenerationSystem | null) => void;
  veriSelectedDocuments: VeriDocumentType[];
  veriSetSelectedDocuments: (documents: VeriDocumentType[]) => void;
  veriLanguage: 'vietnamese' | 'english';
  veriSetLanguage: (language: 'vietnamese' | 'english') => void;
  veriBusinessContext: VeriBusinessProfile | null;
  veriSetBusinessContext: (context: VeriBusinessProfile | null) => void;
  veriAIGenerator: VeriAIDocumentGenerator | null;
  veriSetAIGenerator: (generator: VeriAIDocumentGenerator | null) => void;
}

export interface VeriAIDocumentGenerator {
  veriEngineId: string;
  veriEngineVersion: string;
  veriCapabilities: string[];
  veriLanguages: string[];
  veriDocumentTypes: VeriDocumentType[];
  veriCulturalModels: string[];
  veriAnalysisTypes: string[];
}

// Cultural Formatting Types
export interface VeriCulturalFormatter {
  document_structure: Record<string, VeriDocumentStructure>;
  regional_adaptations: Record<string, VeriRegionalAdaptations>;
  legal_language_adaptations: Record<string, VeriLegalLanguageAdaptation>;
}

export interface VeriDocumentStructure {
  veriHeaderStyle: string;
  veriGreeting: string;
  veriClosing: string;
  veriSignature: string;
  veriFormality: string;
  veriLanguageComplexity: string;
}

export interface VeriLegalLanguageAdaptation {
  veriLegalTerminology: string;
  veriExplanationLevel: string;
  veriExampleUsage: string;
  veriComplexitySentences: string;
}

