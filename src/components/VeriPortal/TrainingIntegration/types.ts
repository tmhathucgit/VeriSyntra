// VeriPortal_04_TrainingIntegration TypeScript Types
// Vietnamese PDPL 2025 Training & Education System Types

// Core Vietnamese Training Integration Engine
export interface VeriTrainingIntegrationSystem {
  veriTrainingId: string;
  veriTrainingProgram: VeriTrainingProgram;
  veriLearnerProfile: VeriLearnerProfile;
  veriLearningPath: VeriLearningPath[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriCulturalAdaptations: VeriCulturalLearningAdaptations;
  veriProgressTracking: VeriProgressTracking;
  veriAIPersonalization: VeriAIPersonalization;
  veriCertificationStatus: VeriCertificationStatus;
}

// Vietnamese Training Program Types
export type VeriTrainingProgramType = 
  | 'pdpl-2025-fundamentals'
  | 'data-protection-management'
  | 'privacy-policy-implementation'
  | 'security-incident-response'
  | 'data-subject-rights-management'
  | 'cross-border-data-transfer'
  | 'dpo-certification'
  | 'employee-privacy-awareness'
  | 'vendor-privacy-management'
  | 'compliance-audit-preparation';

// Vietnamese Training Program Interface
export interface VeriTrainingProgram {
  veriProgramId: string;
  veriProgramType: VeriTrainingProgramType;
  veriProgramName: string;
  veriProgramNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriDuration: VeriTrainingDuration;
  veriDifficultyLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriLearningObjectives: VeriLearningObjective[];
  veriPrerequisites: string[];
  veriCertificationLevel: 'basic' | 'professional' | 'expert';
  veriTargetRoles: VeriBusinessRole[];
  veriIndustryFocus: string[];
  veriCulturalAdaptations: VeriCulturalLearningAdaptations;
}

// Vietnamese Learner Profile Context
export interface VeriLearnerProfile {
  veriLearnerId: string;
  veriRole: VeriBusinessRole;
  veriExperienceLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriLearningStyle: VeriLearningStyle;
  veriBusinessContext: VeriBusinessContext;
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriCulturalPreferences: VeriCulturalLearningPreferences;
  veriAvailableTime: VeriTimeAvailability;
  veriLearningGoals: VeriLearningGoal[];
  veriLearningHistory: VeriLearningHistoryRecord[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriAssessmentResults: VeriAssessmentResult[];
}

// Vietnamese Business Role Context
export interface VeriBusinessRole {
  veriRoleId: string;
  veriRoleType: 'executive' | 'manager' | 'staff' | 'dpo' | 'it-admin' | 'legal-counsel';
  veriRoleName: string;
  veriRoleNameVi: string;
  veriResponsibilities: string[];
  veriComplianceRequirements: string[];
  veriDecisionMakingLevel: 'strategic' | 'operational' | 'tactical';
  veriTeamSize: number;
  veriReportingLevel: number;
}

// Vietnamese Learning Style Preferences
export interface VeriLearningStyle {
  veriLearningPreference: 'visual' | 'auditory' | 'kinesthetic' | 'reading' | 'mixed';
  veriContentDepth: 'overview' | 'detailed' | 'comprehensive' | 'expert';
  veriInteractionStyle: 'self-paced' | 'guided' | 'collaborative' | 'mentored';
  veriAssessmentPreference: 'frequent-checkpoints' | 'module-assessments' | 'comprehensive-exams';
  veriPacingPreference: 'accelerated' | 'standard' | 'extended' | 'flexible';
  veriMediaPreference: 'text' | 'video' | 'interactive' | 'mixed-media';
}

// Vietnamese Cultural Learning Preferences
export interface VeriCulturalLearningPreferences {
  veriCommunicationStyle: 'formal' | 'consultative' | 'collaborative' | 'direct';
  veriHierarchyRespect: 'high' | 'moderate' | 'low';
  veriGroupLearningComfort: 'individual' | 'small-group' | 'large-group' | 'mixed';
  veriAuthorityReliance: 'expert-guided' | 'peer-collaborative' | 'self-directed';
  veriErrorToleranceStyle: 'perfectionist' | 'progressive' | 'experimental';
  veriCulturalExamplePreference: 'local' | 'international' | 'mixed';
  veriLanguageComplexity: 'simple' | 'moderate' | 'complex' | 'technical';
}

// Vietnamese Time Availability
export interface VeriTimeAvailability {
  veriWeeklyHours: number;
  veriSessionLength: number; // minutes
  veriPreferredTimes: VeriPreferredLearningTime[];
  veriFlexibility: 'rigid' | 'moderate' | 'flexible';
  veriDeadlinePressure: 'urgent' | 'moderate' | 'flexible';
  veriLearningSchedule: 'intensive' | 'distributed' | 'as-needed';
}

export interface VeriPreferredLearningTime {
  veriDay: 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday';
  veriTimeSlot: 'morning' | 'afternoon' | 'evening' | 'night';
  veriAvailability: 'preferred' | 'available' | 'unavailable';
}

// Vietnamese Learning Goals
export interface VeriLearningGoal {
  veriGoalId: string;
  veriGoalType: 'certification' | 'compliance' | 'skill-development' | 'career-advancement';
  veriGoalName: string;
  veriGoalNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriPriority: 'critical' | 'high' | 'medium' | 'low';
  veriTargetCompletionDate: Date;
  veriMeasurableOutcomes: VeriMeasurableOutcome[];
  veriBusinessJustification: string;
}

export interface VeriMeasurableOutcome {
  veriOutcomeId: string;
  veriOutcomeName: string;
  veriOutcomeNameVi: string;
  veriMeasurementCriteria: string;
  veriSuccessThreshold: number;
  veriCurrentProgress: number;
}

// Vietnamese Learning Path Structure
export interface VeriLearningPath {
  veriPathId: string;
  veriLearnerProfile: VeriLearnerProfile;
  veriTrainingProgram: VeriTrainingProgram;
  veriPersonalizedModules: VeriTrainingModule[];
  veriAdaptiveAssessments: VeriAdaptiveAssessment[];
  veriEstimatedDuration: VeriTrainingDuration;
  veriLearningObjectives: VeriPersonalizedLearningObjective[];
  veriCulturalLearningElements: VeriCulturalLearningElement[];
  veriProgressMilestones: VeriProgressMilestone[];
  veriPersonalizationScore: number;
}

// Vietnamese Training Module
export interface VeriTrainingModule {
  veriModuleId: string;
  veriModuleType: VeriModuleType;
  veriModuleName: string;
  veriModuleNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriLearningContent: VeriLearningContent;
  veriInteractiveElements: VeriInteractiveElement[];
  veriAssessments: VeriKnowledgeAssessment[];
  veriPracticalExercises: VeriPracticalExercise[];
  veriEstimatedTime: number; // minutes
  veriDifficultyLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriPrerequisites: string[];
  veriLearningObjectives: VeriModuleLearningObjective[];
  veriCulturalAdaptations: VeriModuleCulturalAdaptation[];
}

export type VeriModuleType = 
  | 'introduction'
  | 'concept-learning'
  | 'practical-application'
  | 'case-study'
  | 'simulation'
  | 'assessment'
  | 'certification';

// Vietnamese Learning Content Structure
export interface VeriLearningContent {
  veriContentId: string;
  veriContentType: VeriContentType;
  veriSections: VeriContentSection[];
  veriMultimediaElements: VeriMultimediaElement[];
  veriInteractiveComponents: VeriInteractiveComponent[];
  veriCulturalExamples: VeriCulturalExample[];
  veriLanguageVersions: VeriLanguageVersion[];
  veriPersonalizationLevel: number;
}

export type VeriContentType = 
  | 'text-content'
  | 'video-content'
  | 'interactive-content'
  | 'multimedia-content'
  | 'scenario-content'
  | 'assessment-content';

export interface VeriContentSection {
  veriSectionId: string;
  veriSectionType: VeriSectionType;
  veriTitle: string;
  veriTitleVi: string;
  veriContent: string;
  veriContentVi: string;
  veriEstimatedReadTime: number;
  veriKeyPoints: VeriKeyPoint[];
  veriVisualAids: VeriVisualAid[];
  veriInteractionPoints: VeriInteractionPoint[];
}

export type VeriSectionType = 
  | 'introduction'
  | 'concept-explanation'
  | 'example-illustration'
  | 'practical-application'
  | 'knowledge-check'
  | 'summary';

// Vietnamese Cultural Learning Adaptations
export interface VeriCulturalLearningAdaptations {
  veriRegionalAdaptation: VeriRegionalLearningAdaptation;
  veriBusinessRoleAdaptation: VeriBusinessRoleLearningAdaptation;
  veriIndustrySpecificAdaptation: VeriIndustryLearningAdaptation;
  veriLanguageAdaptations: VeriLanguageLearningAdaptation;
  veriCulturalExampleSet: VeriCulturalExampleSet;
  veriLearningStyleAdaptation: VeriLearningStyleAdaptation;
}

export interface VeriRegionalLearningAdaptation {
  veriRegion: 'north' | 'central' | 'south';
  veriLearningApproach: string;
  veriContentDepth: string;
  veriAssessmentStyle: string;
  veriInteractionStyle: string;
  veriPacing: string;
  veriCulturalExamples: string;
  veriCommunicationTone: string;
  veriHierarchyConsideration: string;
}

export interface VeriBusinessRoleLearningAdaptation {
  veriRole: VeriBusinessRole;
  veriContentFocus: string;
  veriTimeInvestment: string;
  veriLearningFormat: string;
  veriAssessmentType: string;
  veriCulturalTone: string;
  veriPracticalApplications: VeriPracticalApplication[];
  veriRoleSpecificScenarios: VeriRoleSpecificScenario[];
}

// Vietnamese Progress Tracking
export interface VeriProgressTracking {
  veriTrackingId: string;
  veriLearnerProfile: VeriLearnerProfile;
  veriCurrentModule: VeriTrainingModule;
  veriOverallProgress: number; // percentage
  veriModuleProgress: VeriModuleProgressRecord[];
  veriAssessmentResults: VeriAssessmentResult[];
  veriLearningAnalytics: VeriLearningAnalytics;
  veriEngagementMetrics: VeriEngagementMetrics;
  veriLearningVelocity: VeriLearningVelocity;
  veriKnowledgeRetention: VeriKnowledgeRetention;
  veriPersonalizationEffectiveness: VeriPersonalizationEffectiveness;
}

export interface VeriModuleProgressRecord {
  veriModuleId: string;
  veriModuleName: string;
  veriStartDate: Date;
  veriCompletionDate?: Date;
  veriTimeSpent: number; // minutes
  veriProgressPercentage: number;
  veriSectionProgress: VeriSectionProgress[];
  veriAssessmentScores: VeriAssessmentScore[];
  veriEngagementLevel: 'low' | 'medium' | 'high';
  veriDifficultyRating: number; // 1-5 scale
  veriSatisfactionRating?: number; // 1-5 scale
}

// Vietnamese AI Personalization
export interface VeriAIPersonalization {
  veriPersonalizationId: string;
  veriLearnerAnalysis: VeriLearnerAnalysis;
  veriContentPersonalization: VeriContentPersonalization;
  veriLearningPathOptimization: VeriLearningPathOptimization;
  veriAssessmentPersonalization: VeriAssessmentPersonalization;
  veriCulturalPersonalization: VeriCulturalPersonalization;
  veriAdaptiveRecommendations: VeriAdaptiveRecommendation[];
  veriPersonalizationScore: number;
  veriEffectivenessMetrics: VeriPersonalizationEffectivenessMetrics;
}

export interface VeriLearnerAnalysis {
  veriAnalysisId: string;
  veriLearnerDimensions: VeriLearnerDimensions;
  veriLearningPredictions: VeriLearningPredictions;
  veriOptimalLearningPath: VeriOptimalLearningPath;
  veriPersonalizationPotential: number;
  veriAIRecommendations: VeriAIRecommendation[];
  veriCulturalLearningAdaptations: VeriCulturalLearningAdaptations;
}

export interface VeriLearnerDimensions {
  veriRoleRequirements: VeriRoleRequirements;
  veriExperienceAssessment: VeriExperienceAssessment;
  veriLearningStyleAnalysis: VeriLearningStyleAnalysis;
  veriCulturalLearningProfile: VeriCulturalLearningProfile;
  veriTimeConstraints: VeriTimeConstraints;
  veriMotivationFactors: VeriMotivationFactors;
}

// Vietnamese Certification Status
export interface VeriCertificationStatus {
  veriCertificationId: string;
  veriCertificationType: VeriCertificationType;
  veriCertificationLevel: 'basic' | 'professional' | 'expert';
  veriCurrentStatus: 'not-started' | 'in-progress' | 'assessment-ready' | 'certified' | 'expired';
  veriRequirements: VeriCertificationRequirement[];
  veriProgress: VeriCertificationProgress;
  veriAssessmentResults: VeriCertificationAssessmentResult[];
  veriIssuedDate?: Date;
  veriExpiryDate?: Date;
  veriRenewalRequirements?: VeriRenewalRequirement[];
  veriCertificateNumber?: string;
  veriVerificationCode?: string;
}

export type VeriCertificationType = 
  | 'pdpl-2025-fundamentals'
  | 'data-protection-professional'
  | 'dpo-certified'
  | 'privacy-implementation-specialist'
  | 'compliance-auditor'
  | 'trainer-certification';

// Vietnamese Adaptive Assessment Types
export interface VeriAdaptiveAssessment {
  veriAssessmentId: string;
  veriAssessmentType: VeriAssessmentType;
  veriLearnerProfile: VeriLearnerProfile;
  veriAdaptiveQuestions: VeriAdaptiveQuestion[];
  veriBusinessScenarios: VeriBusinessScenario[];
  veriAssessmentCriteria: VeriAssessmentCriteria;
  veriCulturalConsiderations: VeriCulturalConsideration[];
  veriEstimatedDuration: number; // minutes
  veriDifficultyAdaptation: VeriDifficultyAdaptation;
  veriPersonalizationLevel: number;
}

export type VeriAssessmentType = 
  | 'knowledge-check'
  | 'module-assessment'
  | 'comprehensive-exam'
  | 'practical-application'
  | 'scenario-based'
  | 'certification-exam';

export interface VeriAdaptiveQuestion {
  veriQuestionId: string;
  veriQuestionType: VeriQuestionType;
  veriQuestion: string;
  veriQuestionVi: string;
  veriOptions?: VeriQuestionOption[];
  veriCorrectAnswer: string | string[];
  veriExplanation: string;
  veriExplanationVi: string;
  veriDifficultyLevel: 'easy' | 'medium' | 'hard' | 'expert';
  veriLearningObjective: string;
  veriCulturalContext: VeriCulturalContext;
  veriBusinessRelevance: VeriBusinessRelevance;
}

export type VeriQuestionType = 
  | 'multiple-choice'
  | 'multiple-select'
  | 'true-false'
  | 'short-answer'
  | 'essay'
  | 'scenario-analysis'
  | 'practical-application';

// Vietnamese Training Integration Props
export interface VeriTrainingIntegrationProps {
  veriLearnerProfile?: VeriLearnerProfile;
  veriLanguage?: 'vietnamese' | 'english';
  veriOnComplete?: (result: VeriTrainingCompletionResult) => void;
  veriOnProgressUpdate?: (progress: VeriProgressUpdate) => void;
  veriCulturalStyle?: string;
  veriSelectedPrograms?: VeriTrainingProgramType[];
}

export interface VeriTrainingCompletionResult {
  veriLearnerProfile: VeriLearnerProfile;
  veriCompletedPrograms: VeriCompletedProgram[];
  veriCertificationsEarned: VeriCertificationStatus[];
  veriOverallProgress: VeriOverallProgress;
  veriLearningAnalytics: VeriLearningAnalytics;
  veriRecommendations: VeriTrainingRecommendation[];
  veriCompletionDate: Date;
}

export interface VeriProgressUpdate {
  veriUpdateId: string;
  veriUpdateType: 'module-progress' | 'assessment-complete' | 'milestone-reached';
  veriCurrentProgress: number;
  veriModuleProgress?: VeriModuleProgressRecord;
  veriAssessmentResult?: VeriAssessmentResult;
  veriMilestone?: VeriProgressMilestone;
  veriUpdateTimestamp: Date;
}

// Vietnamese Training Duration
export interface VeriTrainingDuration {
  veriTotalMinutes: number;
  veriEstimatedSessions: number;
  veriAverageSessionLength: number;
  veriSelfPacedFlexibility: boolean;
  veriMinimumTimeCommitment: number;
  veriMaximumTimeCommitment: number;
  veriPersonalizedEstimate?: number;
}

// Additional supporting interfaces
export interface VeriBusinessContext {
  veriCompanyName: string;
  veriIndustryType: string;
  veriCompanySize: 'startup' | 'sme' | 'enterprise';
  veriDataProcessingVolume: 'low' | 'medium' | 'high';
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriComplianceMaturity: 'beginner' | 'intermediate' | 'advanced';
}

export interface VeriLearningObjective {
  veriObjectiveId: string;
  veriObjectiveName: string;
  veriObjectiveNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriMeasurableCriteria: string;
  veriAssessmentMethod: string;
  veriBloomLevel: 'remember' | 'understand' | 'apply' | 'analyze' | 'evaluate' | 'create';
}

// Vietnamese Training AI Engine Types
export interface VeriAITrainingEngine {
  veriEngineId: string;
  veriVersion: string;
  veriCapabilities: VeriAICapability[];
  veriLanguages: ('vietnamese' | 'english')[];
  veriCulturalModels: string[];
  veriAnalysisTypes: VeriAnalysisType[];
  veriPersonalizationAlgorithms: VeriPersonalizationAlgorithm[];
}

export type VeriAICapability = 
  | 'learner-analysis'
  | 'content-personalization'
  | 'adaptive-assessment'
  | 'cultural-adaptation'
  | 'progress-prediction'
  | 'recommendation-engine';

export type VeriAnalysisType = 
  | 'learning-style-analysis'
  | 'knowledge-gap-analysis'
  | 'cultural-preference-analysis'
  | 'engagement-analysis'
  | 'performance-prediction';

export interface VeriPersonalizationAlgorithm {
  veriAlgorithmName: string;
  veriAlgorithmType: 'machine-learning' | 'rule-based' | 'hybrid';
  veriAccuracyScore: number;
  veriApplicationDomain: string[];
}

// Additional Missing Interface Definitions
export interface VeriLearningHistoryRecord {
  veriRecordId: string;
  veriProgramId: string;
  veriCompletionDate: Date;
  veriScore: number;
  veriTimeSpent: number;
  veriDifficultyLevel: 'easy' | 'medium' | 'hard';
}

export interface VeriAssessmentResult {
  veriResultId: string;
  veriAssessmentId: string;
  veriScore: number;
  veriMaxScore: number;
  veriCompletionTime: number;
  veriAttemptNumber: number;
  veriCompletedAt: Date;
}

export interface VeriPersonalizedLearningObjective {
  veriObjectiveId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriDifficultyLevel: string;
  veriPersonalizationReason: string;
}

export interface VeriCulturalLearningElement {
  veriElementId: string;
  veriType: 'example' | 'case-study' | 'cultural-note';
  veriRegion: 'north' | 'central' | 'south';
  veriContent: string;
  veriContentVi: string;
}

export interface VeriProgressMilestone {
  veriMilestoneId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriRequiredScore: number;
  veriIsAchieved: boolean;
  veriAchievedAt?: Date;
}

export interface VeriInteractiveElement {
  veriElementId: string;
  veriType: 'quiz' | 'simulation' | 'case-study' | 'discussion';
  veriTitle: string;
  veriTitleVi: string;
  veriContent: any;
  veriEstimatedTime: number;
}

export interface VeriKnowledgeAssessment {
  veriAssessmentId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriQuestions: any[];
  veriPassingScore: number;
  veriTimeLimit: number;
}

export interface VeriPracticalExercise {
  veriExerciseId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriSteps: string[];
  veriExpectedOutcome: string;
}

export interface VeriModuleLearningObjective {
  veriObjectiveId: string;
  veriModuleId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriMeasurableCriteria: string;
}

export interface VeriModuleCulturalAdaptation {
  veriAdaptationId: string;
  veriRegion: 'north' | 'central' | 'south';
  veriContentModifications: string[];
  veriExampleReplacements: any[];
}

export interface VeriMultimediaElement {
  veriElementId: string;
  veriType: 'video' | 'audio' | 'image' | 'document';
  veriUrl: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDuration?: number;
}

export interface VeriInteractiveComponent {
  veriComponentId: string;
  veriType: 'button' | 'form' | 'slider' | 'dropdown';
  veriLabel: string;
  veriLabelVi: string;
  veriAction: string;
  veriValidation?: any;
}

export interface VeriCulturalExample {
  veriExampleId: string;
  veriRegion: 'north' | 'central' | 'south';
  veriIndustry: string;
  veriScenario: string;
  veriScenarioVi: string;
  veriLessonLearned: string;
}

export interface VeriLanguageVersion {
  veriLanguage: 'vietnamese' | 'english';
  veriContent: string;
  veriAudioUrl?: string;
  veriTranslationQuality: number;
}

export interface VeriKeyPoint {
  veriPointId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriImportanceLevel: 'critical' | 'important' | 'supplementary';
  veriExplanation: string;
  veriExplanationVi: string;
}

export interface VeriVisualAid {
  veriAidId: string;
  veriType: 'diagram' | 'chart' | 'infographic' | 'flowchart';
  veriUrl: string;
  veriDescription: string;
  veriDescriptionVi: string;
}

export interface VeriInteractionPoint {
  veriPointId: string;
  veriType: 'click' | 'hover' | 'input' | 'selection';
  veriTrigger: string;
  veriResponse: string;
  veriResponseVi: string;
}

export interface VeriIndustryLearningAdaptation {
  veriIndustry: string;
  veriSpecificRequirements: string[];
  veriComplianceReferences: string[];
  veriExampleModifications: any[];
}

export interface VeriLanguageLearningAdaptation {
  veriLanguage: 'vietnamese' | 'english';
  veriContentAdaptations: string[];
  veriCulturalNuances: string[];
  veriLocalTerminology: any;
}

export interface VeriCulturalExampleSet {
  veriRegion: 'north' | 'central' | 'south';
  veriExamples: VeriCulturalExample[];
  veriBusinessContexts: string[];
  veriCommunicationStyles: string[];
}

export interface VeriLearningStyleAdaptation {
  veriLearningStyle: 'visual' | 'auditory' | 'kinesthetic' | 'reading' | 'mixed';
  veriContentFormat: string;
  veriInteractionStyle: string;
  veriAssessmentFormat: string;
}

export interface VeriPracticalApplication {
  veriApplicationId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriScenario: string;
  veriScenarioVi: string;
  veriSteps: string[];
  veriExpectedResult: string;
}

export interface VeriRoleSpecificScenario {
  veriScenarioId: string;
  veriRoleType: 'executive' | 'manager' | 'staff' | 'dpo' | 'it-admin' | 'legal-counsel';
  veriTitle: string;
  veriTitleVi: string;
  veriSituation: string;
  veriSituationVi: string;
  veriRequiredActions: string[];
}

export interface VeriLearningAnalytics {
  veriEngagementTime: number;
  veriCompletionRate: number;
  veriRetentionRate: number;
  veriDifficultyProgression: string;
  veriLearningVelocity: number;
}

export interface VeriEngagementMetrics {
  veriTimeSpent: number;
  veriInteractionCount: number;
  veriAttentionScore: number;
  veriParticipationLevel: 'high' | 'medium' | 'low';
}

export interface VeriLearningVelocity {
  veriCurrentPace: number;
  veriOptimalPace: number;
  veriAcceleration: number;
  veriPredictedCompletion: Date;
}

export interface VeriKnowledgeRetention {
  veriShortTermRetention: number;
  veriLongTermRetention: number;
  veriRetentionCurve: number[];
  veriForgetfulnessRate: number;
}

export interface VeriPersonalizationEffectiveness {
  veriEffectivenessScore: number;
  veriImprovementAreas: string[];
  veriSuccessMetrics: any;
  veriRecommendations: string[];
}

export interface VeriSectionProgress {
  veriSectionId: string;
  veriCompletionPercentage: number;
  veriTimeSpent: number;
  veriLastAccessed: Date;
  veriDifficulty: 'easy' | 'medium' | 'hard';
}

export interface VeriAssessmentScore {
  veriAssessmentId: string;
  veriScore: number;
  veriMaxScore: number;
  veriPercentage: number;
  veriAttemptNumber: number;
  veriCompletedAt: Date;
}

export interface VeriContentPersonalization {
  veriPersonalizationLevel: 'low' | 'medium' | 'high';
  veriAdaptedElements: string[];
  veriUserPreferences: any;
  veriEffectiveness: number;
}

export interface VeriLearningPathOptimization {
  veriOptimizationScore: number;
  veriRecommendedChanges: string[];
  veriPredictedImprovement: number;
  veriConfidenceLevel: number;
}

export interface VeriAssessmentPersonalization {
  veriDifficultyLevel: 'adaptive' | 'fixed';
  veriQuestionTypes: string[];
  veriAdaptationStrategy: string;
  veriPersonalizationRules: any[];
}

export interface VeriCulturalPersonalization {
  veriRegionalAdaptation: 'north' | 'central' | 'south';
  veriCulturalElements: string[];
  veriLanguagePreference: 'vietnamese' | 'english';
  veriCommunicationStyle: string;
}

export interface VeriAdaptiveRecommendation {
  veriRecommendationId: string;
  veriType: 'content' | 'pacing' | 'difficulty' | 'methodology';
  veriDescription: string;
  veriDescriptionVi: string;
  veriPriority: 'high' | 'medium' | 'low';
  veriImplementation: string;
}

export interface VeriPersonalizationEffectivenessMetrics {
  veriOverallEffectiveness: number;
  veriUserSatisfaction: number;
  veriLearningOutcomeImprovement: number;
  veriEngagementIncrease: number;
}

export interface VeriLearningPredictions {
  veriCompletionPrediction: Date;
  veriSuccessProbability: number;
  veriRiskFactors: string[];
  veriRecommendedInterventions: string[];
}

export interface VeriOptimalLearningPath {
  veriPathId: string;
  veriModuleSequence: string[];
  veriEstimatedDuration: number;
  veriDifficultyProgression: string;
  veriPersonalizationLevel: number;
}

export interface VeriAIRecommendation {
  veriRecommendationId: string;
  veriType: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriConfidence: number;
  veriImplementationSteps: string[];
}

export interface VeriRoleRequirements {
  veriRoleType: string;
  veriRequiredKnowledge: string[];
  veriRequiredSkills: string[];
  veriComplianceRequirements: string[];
  veriCertificationNeeds: string[];
}

export interface VeriExperienceAssessment {
  veriCurrentLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriKnowledgeGaps: string[];
  veriStrengths: string[];
  veriRecommendedPrograms: string[];
}

export interface VeriLearningStyleAnalysis {
  veriPrimaryStyle: 'visual' | 'auditory' | 'kinesthetic' | 'reading' | 'mixed';
  veriSecondaryStyle: string;
  veriEffectivenessScore: number;
  veriAdaptationNeeds: string[];
}

export interface VeriCulturalLearningProfile {
  veriRegion: 'north' | 'central' | 'south';
  veriCommunicationPreferences: string[];
  veriLearningApproaches: string[];
  veriCulturalSensitivities: string[];
}

export interface VeriTimeConstraints {
  veriAvailableHoursPerWeek: number;
  veriPreferredLearningTimes: string[];
  veriDeadlines: Date[];
  veriFlexibilityLevel: 'high' | 'medium' | 'low';
}

export interface VeriMotivationFactors {
  veriIntrinsicMotivators: string[];
  veriExtrinsicMotivators: string[];
  veriMotivationLevel: 'high' | 'medium' | 'low';
  veriBarriers: string[];
}

export interface VeriCertificationRequirement {
  veriRequirementId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriRequired: boolean;
  veriCompleted: boolean;
}

export interface VeriCertificationProgress {
  veriCompletionPercentage: number;
  veriRequirementsMet: number;
  veriTotalRequirements: number;
  veriEstimatedCompletion: Date;
}

export interface VeriCertificationAssessmentResult {
  veriAssessmentId: string;
  veriScore: number;
  veriMaxScore: number;
  veriPassingScore: number;
  veriPassed: boolean;
  veriCompletedAt: Date;
}

export interface VeriRenewalRequirement {
  veriRequirementId: string;
  veriType: 'continuing-education' | 'reassessment' | 'documentation';
  veriDescription: string;
  veriDescriptionVi: string;
  veriDueDate: Date;
  veriCompleted: boolean;
}

export interface VeriBusinessScenario {
  veriScenarioId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriIndustry: string;
  veriComplexityLevel: 'simple' | 'moderate' | 'complex';
  veriExpectedOutcome: string;
}

export interface VeriAssessmentCriteria {
  veriCriteriaId: string;
  veriName: string;
  veriNameVi: string;
  veriWeightPercentage: number;
  veriPassingThreshold: number;
  veriEvaluationMethod: string;
}

export interface VeriBusinessRelevance {
  veriRelevanceScore: number;
  veriIndustryAlignment: string[];
  veriRoleApplicability: string[];
  veriPracticalApplications: string[];
  veriImpactLevel: 'high' | 'medium' | 'low';
}

export interface VeriTrainingRecommendation {
  veriRecommendationId: string;
  veriType: 'program' | 'module' | 'resource' | 'methodology';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriPriority: 'high' | 'medium' | 'low';
  veriReasoning: string;
  veriReasoningVi: string;
  veriExpectedBenefit: string;
}

export interface VeriCulturalConsideration {
  veriConsiderationId: string;
  veriType: 'communication-style' | 'hierarchy-respect' | 'time-orientation' | 'learning-preference';
  veriDescription: string;
  veriDescriptionVi: string;
  veriRegion: 'north' | 'central' | 'south';
  veriImpact: 'high' | 'medium' | 'low';
  veriAdaptationStrategy: string;
}

export interface VeriDifficultyAdaptation {
  veriCurrentLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriTargetLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriAdaptationRules: string[];
  veriProgressionRate: number;
  veriSupportLevel: 'high' | 'medium' | 'low';
}

export interface VeriQuestionOption {
  veriOptionId: string;
  veriOptionText: string;
  veriOptionTextVi: string;
  veriIsCorrect: boolean;
  veriExplanation?: string;
  veriExplanationVi?: string;
  veriWeight?: number;
}

export interface VeriCulturalContext {
  veriContextId: string;
  veriRegion: 'north' | 'central' | 'south';
  veriBusinessCulture: string;
  veriCommunicationNorms: string[];
  veriHierarchyStructure: string;
  veriDecisionMakingStyle: string;
  veriTimeOrientation: string;
}

export interface VeriCompletedProgram {
  veriProgramId: string;
  veriProgramTitle: string;
  veriProgramTitleVi: string;
  veriCompletionDate: Date;
  veriFinalScore: number;
  veriCertificationEarned?: string;
  veriTimeInvestment: number;
}

export interface VeriOverallProgress {
  veriTotalProgramsStarted: number;
  veriTotalProgramsCompleted: number;
  veriCompletionRate: number;
  veriAverageScore: number;
  veriTotalTimeInvested: number;
  veriCurrentActivePrograms: number;
  veriCertificationsEarned: number;
}

// Import extended types
export * from './extendedTypes';

// Export all types for use in components and services
export * from './types';