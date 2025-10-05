// Extended TypeScript Types for Vietnamese Training Integration System
// Supporting types for comprehensive PDPL 2025 training platform

// Forward type declarations to avoid circular imports
export type VeriAssessmentType = 
  | 'knowledge-check'
  | 'module-assessment'
  | 'comprehensive-exam'
  | 'practical-application'
  | 'scenario-based'
  | 'certification-exam';

// Basic interfaces for type references
export interface VeriLearnerProfile {
  veriLearnerId: string;
  // Full definition in main types file
}

export interface VeriLearningObjective {
  veriObjectiveId: string;
  veriObjectiveName: string;
  // Full definition in main types file
}

// Vietnamese Learning History Types
export interface VeriLearningHistoryRecord {
  veriRecordId: string;
  veriModuleId: string;
  veriModuleName: string;
  veriCompletionDate: Date;
  veriScore: number;
  veriTimeSpent: number; // minutes
  veriDifficultyLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  veriEngagementLevel: 'low' | 'medium' | 'high';
  veriSatisfactionRating: number; // 1-5 scale
  veriRetentionScore?: number;
}

// Vietnamese Assessment Result Types
export interface VeriAssessmentResult {
  veriResultId: string;
  veriAssessmentId: string;
  veriAssessmentType: VeriAssessmentType;
  veriScore: number;
  veriMaxScore: number;
  veriPercentage: number;
  veriPassingThreshold: number;
  veriPassed: boolean;
  veriCompletionDate: Date;
  veriTimeSpent: number; // minutes
  veriAttemptNumber: number;
  veriQuestionResults: VeriQuestionResult[];
  veriAnalytics: VeriAssessmentAnalytics;
}

export interface VeriQuestionResult {
  veriQuestionId: string;
  veriAnswerProvided: string | string[];
  veriCorrectAnswer: string | string[];
  veriIsCorrect: boolean;
  veriTimeSpent: number; // seconds
  veriDifficultyLevel: 'easy' | 'medium' | 'hard' | 'expert';
  veriLearningObjective: string;
}

export interface VeriAssessmentAnalytics {
  veriAnalyticsId: string;
  veriStrengthAreas: string[];
  veriImprovementAreas: string[];
  veriKnowledgeGaps: string[];
  veriRecommendedReview: string[];
  veriPerformanceTrend: 'improving' | 'stable' | 'declining';
  veriConfidenceLevel: number;
}

// Vietnamese Personalized Learning Objective Types
export interface VeriPersonalizedLearningObjective {
  veriObjectiveId: string;
  veriLearnerProfile: VeriLearnerProfile;
  veriBaseObjective: VeriLearningObjective;
  veriPersonalizedContent: string;
  veriPersonalizedContentVi: string;
  veriPersonalizationLevel: number;
  veriCulturalAdaptation: string;
  veriRoleSpecificContext: string;
  veriPracticality: number; // relevance score
  veriEstimatedAchievementTime: number; // minutes
}

// Vietnamese Cultural Learning Element Types
export interface VeriCulturalLearningElement {
  veriElementId: string;
  veriElementType: 'example' | 'scenario' | 'case-study' | 'cultural-note' | 'context-explanation';
  veriTitle: string;
  veriTitleVi: string;
  veriContent: string;
  veriContentVi: string;
  veriCulturalRelevance: VeriCulturalRelevance;
  veriRegionalAdaptation: 'north' | 'central' | 'south' | 'national';
  veriBusinessContext: string;
  veriLearningValue: number;
}

export interface VeriCulturalRelevance {
  veriRelevanceScore: number; // 1-10
  veriCulturalAspect: string;
  veriBusinessImpact: string;
  veriLearningConnection: string;
  veriLocalExample: boolean;
}

// Vietnamese Progress Milestone Types
export interface VeriProgressMilestone {
  veriMilestoneId: string;
  veriMilestoneType: 'module-completion' | 'assessment-passed' | 'skill-mastered' | 'certification-earned';
  veriMilestoneName: string;
  veriMilestoneNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriProgressThreshold: number; // percentage
  veriAchieved: boolean;
  veriAchievedDate?: Date;
  veriRewards: VeriMilestoneReward[];
  veriNextSteps: string[];
}

export interface VeriMilestoneReward {
  veriRewardId: string;
  veriRewardType: 'badge' | 'certificate' | 'points' | 'recognition';
  veriRewardName: string;
  veriRewardNameVi: string;
  veriDescription: string;
  veriValue: number;
}

// Vietnamese Interactive Element Types
export interface VeriInteractiveElement {
  veriElementId: string;
  veriElementType: 'quiz' | 'drag-drop' | 'simulation' | 'scenario' | 'calculator' | 'checklist';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriInstructions: string;
  veriInstructionsVi: string;
  veriInteractionData: VeriInteractionData;
  veriEstimatedTime: number; // minutes
  veriLearningObjectives: string[];
}

export interface VeriInteractionData {
  veriDataId: string;
  veriDataType: 'json' | 'xml' | 'custom';
  veriConfiguration: Record<string, any>;
  veriValidationRules: VeriValidationRule[];
  veriFeedbackMessages: VeriFeedbackMessage[];
}

export interface VeriValidationRule {
  veriRuleId: string;
  veriCondition: string;
  veriErrorMessage: string;
  veriErrorMessageVi: string;
}

export interface VeriFeedbackMessage {
  veriMessageId: string;
  veriTrigger: string;
  veriMessage: string;
  veriMessageVi: string;
  veriType: 'success' | 'warning' | 'error' | 'info';
}

// Vietnamese Knowledge Assessment Types
export interface VeriKnowledgeAssessment {
  veriAssessmentId: string;
  veriAssessmentName: string;
  veriAssessmentNameVi: string;
  veriType: VeriAssessmentType;
  veriQuestions: VeriKnowledgeQuestion[];
  veriPassingScore: number;
  veriMaxAttempts: number;
  veriTimeLimit: number; // minutes
  veriShuffleQuestions: boolean;
  veriInstantFeedback: boolean;
}

export interface VeriKnowledgeQuestion {
  veriQuestionId: string;
  veriQuestion: string;
  veriQuestionVi: string;
  veriType: 'multiple-choice' | 'true-false' | 'short-answer' | 'essay';
  veriOptions?: VeriQuestionOption[];
  veriCorrectAnswer: string | string[];
  veriExplanation: string;
  veriExplanationVi: string;
  veriPoints: number;
  veriDifficulty: 'easy' | 'medium' | 'hard';
}

export interface VeriQuestionOption {
  veriOptionId: string;
  veriText: string;
  veriTextVi: string;
  veriIsCorrect: boolean;
}

// Vietnamese Practical Exercise Types
export interface VeriPracticalExercise {
  veriExerciseId: string;
  veriExerciseName: string;
  veriExerciseNameVi: string;
  veriType: 'case-study' | 'simulation' | 'project' | 'workshop' | 'role-play';
  veriDescription: string;
  veriDescriptionVi: string;
  veriObjectives: string[];
  veriMaterials: VeriExerciseMaterial[];
  veriSteps: VeriExerciseStep[];
  veriEvaluationCriteria: VeriEvaluationCriteria[];
  veriEstimatedTime: number; // minutes
  veriDifficultyLevel: 'beginner' | 'intermediate' | 'advanced';
}

export interface VeriExerciseMaterial {
  veriMaterialId: string;
  veriMaterialType: 'document' | 'template' | 'checklist' | 'video' | 'tool';
  veriName: string;
  veriNameVi: string;
  veriDescription: string;
  veriUrl?: string;
  veriContent?: string;
}

export interface VeriExerciseStep {
  veriStepId: string;
  veriStepNumber: number;
  veriInstruction: string;
  veriInstructionVi: string;
  veriExpectedOutcome: string;
  veriEstimatedTime: number; // minutes
  veriResources: string[];
}

export interface VeriEvaluationCriteria {
  veriCriteriaId: string;
  veriCriteriaName: string;
  veriCriteriaNameVi: string;
  veriDescription: string;
  veriMaxScore: number;
  veriRubric: VeriRubricLevel[];
}

export interface VeriRubricLevel {
  veriLevel: 'excellent' | 'good' | 'satisfactory' | 'needs-improvement';
  veriScoreRange: { min: number; max: number };
  veriDescription: string;
  veriDescriptionVi: string;
}

// Vietnamese Module Learning Objective Types
export interface VeriModuleLearningObjective {
  veriObjectiveId: string;
  veriModuleId: string;
  veriObjective: VeriLearningObjective;
  veriModuleSpecificContext: string;
  veriPrerequisiteKnowledge: string[];
  veriAssessmentMethods: string[];
  veriPracticalApplications: string[];
  veriCulturalConsiderations: string[];
}

// Vietnamese Module Cultural Adaptation Types
export interface VeriModuleCulturalAdaptation {
  veriAdaptationId: string;
  veriCulturalAspect: 'communication' | 'hierarchy' | 'learning-style' | 'examples' | 'assessment';
  veriRegionalFocus: 'north' | 'central' | 'south' | 'national';
  veriAdaptationDescription: string;
  veriAdaptationDescriptionVi: string;
  veriImplementationDetails: string;
  veriEffectivenessScore: number;
}

// Vietnamese Multimedia Element Types
export interface VeriMultimediaElement {
  veriElementId: string;
  veriType: 'image' | 'video' | 'audio' | 'animation' | 'infographic' | 'interactive-media';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriUrl: string;
  veriThumbnail?: string;
  veriDuration?: number; // seconds for video/audio
  veriFileSize: number; // bytes
  veriAccessibilityDescription: string;
  veriAccessibilityDescriptionVi: string;
  veriCulturalContext?: string;
}

// Vietnamese Interactive Component Types
export interface VeriInteractiveComponent {
  veriComponentId: string;
  veriType: 'button' | 'slider' | 'dropdown' | 'checkbox' | 'input-field' | 'drag-drop-zone';
  veriLabel: string;
  veriLabelVi: string;
  veriConfiguration: Record<string, any>;
  veriValidation: VeriComponentValidation;
  veriFeedback: VeriComponentFeedback;
  veriAccessibilitySettings: VeriAccessibilitySettings;
}

export interface VeriComponentValidation {
  veriRequired: boolean;
  veriPattern?: string;
  veriMinValue?: number;
  veriMaxValue?: number;
  veriCustomValidation?: string;
}

export interface VeriComponentFeedback {
  veriSuccessMessage: string;
  veriSuccessMessageVi: string;
  veriErrorMessage: string;
  veriErrorMessageVi: string;
  veriHelpText?: string;
  veriHelpTextVi?: string;
}

export interface VeriAccessibilitySettings {
  veriAriaLabel: string;
  veriAriaLabelVi: string;
  veriTabIndex: number;
  veriKeyboardShortcut?: string;
  veriScreenReaderText?: string;
  veriScreenReaderTextVi?: string;
}

// Vietnamese Cultural Example Types
export interface VeriCulturalExample {
  veriExampleId: string;
  veriType: 'business-scenario' | 'legal-case' | 'industry-practice' | 'cultural-norm';
  veriTitle: string;
  veriTitleVi: string;
  veriContext: string;
  veriContextVi: string;
  veriExample: string;
  veriExampleVi: string;
  veriLearningPoints: string[];
  veriLearningPointsVi: string[];
  veriRegionalRelevance: 'north' | 'central' | 'south' | 'national';
  veriIndustryRelevance: string[];
  veriCulturalSignificance: number; // 1-10 scale
}

// Vietnamese Language Version Types
export interface VeriLanguageVersion {
  veriVersionId: string;
  veriLanguage: 'vietnamese' | 'english';
  veriContent: string;
  veriQualityScore: number; // 1-10
  veriCulturalAdaptation: number; // 1-10
  veriLocalizationNotes: string;
  veriReviewStatus: 'draft' | 'reviewed' | 'approved';
  veriLastUpdated: Date;
}

// Vietnamese Key Point Types
export interface VeriKeyPoint {
  veriPointId: string;
  veriPointType: 'definition' | 'important-fact' | 'warning' | 'tip' | 'example';
  veriContent: string;
  veriContentVi: string;
  veriImportanceLevel: 'low' | 'medium' | 'high' | 'critical';
  veriVisualStyle: string;
  veriRelatedConcepts: string[];
}

// Vietnamese Visual Aid Types
export interface VeriVisualAid {
  veriAidId: string;
  veriType: 'diagram' | 'chart' | 'flowchart' | 'timeline' | 'map' | 'illustration';
  veriTitle: string;
  veriTitleVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriImageUrl: string;
  veriAltText: string;
  veriAltTextVi: string;
  veriInteractive: boolean;
  veriCulturalContext?: string;
}

// Vietnamese Interaction Point Types
export interface VeriInteractionPoint {
  veriPointId: string;
  veriType: 'question' | 'reflection' | 'discussion' | 'activity' | 'assessment';
  veriPrompt: string;
  veriPromptVi: string;
  veriExpectedResponse: string;
  veriGuidance: string;
  veriGuidanceVi: string;
  veriEstimatedTime: number; // minutes
  veriSkillLevel: 'basic' | 'intermediate' | 'advanced';
}

// Vietnamese Industry Learning Adaptation Types
export interface VeriIndustryLearningAdaptation {
  veriIndustryType: string;
  veriSpecificRequirements: string[];
  veriContextualExamples: VeriContextualExample[];
  veriRegulatoryFocus: string[];
  veriPracticalApplications: VeriIndustryPracticalApplication[];
  veriCaseStudies: VeriIndustryCaseStudy[];
}

export interface VeriContextualExample {
  veriExampleId: string;
  veriIndustryContext: string;
  veriScenario: string;
  veriScenarioVi: string;
  veriLearningValue: number;
  veriComplexityLevel: 'basic' | 'intermediate' | 'advanced';
}

export interface VeriIndustryPracticalApplication {
  veriApplicationId: string;
  veriApplicationName: string;
  veriApplicationNameVi: string;
  veriDescription: string;
  veriDescriptionVi: string;
  veriSteps: string[];
  veriExpectedOutcomes: string[];
  veriIndustryRelevance: number;
}

export interface VeriIndustryCaseStudy {
  veriCaseStudyId: string;
  veriTitle: string;
  veriTitleVi: string;
  veriBackground: string;
  veriBackgroundVi: string;
  veriChallenge: string;
  veriChallengeVi: string;
  veriSolution: string;
  veriSolutionVi: string;
  veriLessonsLearned: string[];
  veriLessonsLearnedVi: string[];
  veriComplexity: 'basic' | 'intermediate' | 'advanced';
}

// Vietnamese Language Learning Adaptation Types
export interface VeriLanguageLearningAdaptation {
  veriPrimaryLanguage: 'vietnamese' | 'english';
  veriSecondaryLanguage?: 'vietnamese' | 'english';
  veriComplexityLevel: 'simple' | 'moderate' | 'complex' | 'technical';
  veriCulturalNuances: boolean;
  veriLocalTerminology: boolean;
  veriTranslationQuality: number; // 1-10
  veriLocalizationLevel: number; // 1-10
}

// Vietnamese Cultural Example Set Types
export interface VeriCulturalExampleSet {
  veriSetId: string;
  veriTheme: string;
  veriThemeVi: string;
  veriExamples: VeriCulturalExample[];
  veriRegionalVariations: VeriRegionalVariation[];
  veriBusinessApplications: string[];
  veriLearningObjectives: string[];
}

export interface VeriRegionalVariation {
  veriRegion: 'north' | 'central' | 'south';
  veriVariationDescription: string;
  veriVariationDescriptionVi: string;
  veriCulturalContext: string;
  veriBusinessImplications: string[];
}

// Vietnamese Learning Style Adaptation Types
export interface VeriLearningStyleAdaptation {
  veriLearnerProfile: VeriLearnerProfile;
  veriAdaptedContent: VeriAdaptedContent;
  veriAdaptedAssessment: VeriAdaptedAssessment;
  veriAdaptedInteraction: VeriAdaptedInteraction;
  veriPersonalizationScore: number;
  veriEffectivenessMetrics: VeriEffectivenessMetrics;
}

export interface VeriAdaptedContent {
  veriContentFormat: 'visual' | 'auditory' | 'kinesthetic' | 'reading' | 'mixed';
  veriContentDepth: 'summary' | 'standard' | 'detailed' | 'comprehensive';
  veriPresentationStyle: 'linear' | 'modular' | 'exploratory' | 'structured';
  veriInteractionFrequency: 'minimal' | 'moderate' | 'frequent' | 'continuous';
}

export interface VeriAdaptedAssessment {
  veriAssessmentFormat: 'multiple-choice' | 'practical' | 'essay' | 'project' | 'mixed';
  veriAssessmentFrequency: 'continuous' | 'module-based' | 'milestone' | 'final';
  veriFeedbackTiming: 'immediate' | 'delayed' | 'session-end' | 'module-end';
  veriDifficultyCurve: 'gradual' | 'standard' | 'steep' | 'adaptive';
}

export interface VeriAdaptedInteraction {
  veriInteractionStyle: 'guided' | 'exploratory' | 'collaborative' | 'independent';
  veriSocialLearning: 'individual' | 'pair' | 'small-group' | 'large-group';
  veriPeerInteraction: 'none' | 'minimal' | 'moderate' | 'extensive';
  veriMentorSupport: 'none' | 'available' | 'scheduled' | 'continuous';
}

export interface VeriEffectivenessMetrics {
  veriEngagementScore: number;
  veriComprehensionScore: number;
  veriRetentionScore: number;
  veriCompletionRate: number;
  veriSatisfactionScore: number;
  veriLearningVelocity: number;
}

// Export all extended types
export type * from './extendedTypes';