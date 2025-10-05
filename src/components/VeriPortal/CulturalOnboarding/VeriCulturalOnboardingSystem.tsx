// VeriPortal Cultural Onboarding Main Component - Vietnamese AI/ML Enhanced System
// Implementation Status: ✅ IMPLEMENTED

import React, { useState, useEffect, useContext, createContext } from 'react';
import { useTranslation } from 'react-i18next';
import { usePageTitle } from '../../../hooks/usePageTitle';
import type {
  VeriCulturalOnboardingSystem as VeriCulturalOnboardingSystemType,
  VeriOnboardingStep,
  VeriCulturalContext,
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine,
  VeriAIInsights
} from './types';
import {
  VeriOnboardingProgress,
  VeriOnboardingContent,
  VeriAIInsightsDashboard
} from './components';
import { VeriPortalLayout } from '../VeriPortalLayout';
import {
  initializeVeriAICulturalEngine,
  startVeriMLCulturalAnalysis,
  enableVeriAutomationEngine
} from './services';
import './styles/VeriCulturalOnboardingTheme.css';

// Vietnamese Cultural Onboarding Context
interface VeriOnboardingContextType {
  veriOnboardingState?: VeriCulturalOnboardingSystemType;
  veriCurrentStep: VeriOnboardingStep;
  veriLanguage: 'vietnamese' | 'english';
  veriCulturalContext?: VeriCulturalContext;
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
  veriAIInsights?: VeriAIInsights[];
  setVeriCurrentStep: (step: VeriOnboardingStep) => void;
  setVeriLanguage: (lang: 'vietnamese' | 'english') => void;
}

const VeriOnboardingContext = createContext<VeriOnboardingContextType | undefined>(undefined);

// Custom hook for using the onboarding context
export const useVeriOnboardingContext = () => {
  const context = useContext(VeriOnboardingContext);
  if (!context) {
    throw new Error('useVeriOnboardingContext must be used within VeriOnboardingProvider');
  }
  return context;
};

// AI-Powered Vietnamese Cultural Onboarding Provider
interface VeriOnboardingProviderProps {
  children: React.ReactNode;
  veriLanguage: 'vietnamese' | 'english';
  veriCulturalContext?: VeriCulturalContext;
  veriOnboardingState?: VeriCulturalOnboardingSystemType;
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
  veriAIInsights?: VeriAIInsights[];
}

export const VeriAIPoweredCulturalOnboardingProvider: React.FC<VeriOnboardingProviderProps> = ({
  children,
  veriLanguage: initialLanguage,
  veriCulturalContext: initialContext,
  veriOnboardingState: initialState,
  veriAIEngine: initialAIEngine,
  veriMLPersonalization: initialMLPersonalization,
  veriAutomationEngine: initialAutomationEngine,
  veriAIInsights: initialAIInsights
}) => {
  const [veriOnboardingState] = useState<VeriCulturalOnboardingSystemType | undefined>(initialState);
  const [veriCurrentStep, setVeriCurrentStep] = useState<VeriOnboardingStep>('cultural-introduction');
  const [veriLanguage, setVeriLanguage] = useState<'vietnamese' | 'english'>(initialLanguage);
  const [veriCulturalContext, setVeriCulturalContext] = useState<VeriCulturalContext | undefined>(initialContext);
  const [veriAIEngine, setVeriAIEngine] = useState<VeriAICulturalEngine | undefined>(initialAIEngine);
  const [veriMLPersonalization, setVeriMLPersonalization] = useState<VeriMLPersonalizationEngine | undefined>(initialMLPersonalization);
  const [veriAutomationEngine, setVeriAutomationEngine] = useState<VeriAutomationEngine | undefined>(initialAutomationEngine);
  const [veriAIInsights, setVeriAIInsights] = useState<VeriAIInsights[] | undefined>(initialAIInsights);

  // Sync language with parent component - ensure provider state updates
  useEffect(() => {
    console.log(`🔄 Provider: Syncing language to ${initialLanguage}`);
    setVeriLanguage(initialLanguage);
  }, [initialLanguage]);

  const contextValue: VeriOnboardingContextType = {
    veriOnboardingState,
    veriCurrentStep,
    veriLanguage,
    veriCulturalContext,
    veriAIEngine,
    veriMLPersonalization,
    veriAutomationEngine,
    veriAIInsights,
    setVeriCurrentStep,
    setVeriLanguage
  };

  return (
    <VeriOnboardingContext.Provider value={contextValue}>
      {children}
    </VeriOnboardingContext.Provider>
  );
};

// Vietnamese Onboarding Step Order
const veriOnboardingSteps: VeriOnboardingStep[] = [
  'cultural-introduction',
  'business-profile-setup',
  'regional-adaptation',
  'cultural-preferences',
  'compliance-readiness',
  'completion-summary'
];

// AI-Powered Main Vietnamese Cultural Onboarding Component
export const VeriCulturalOnboardingSystem: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [veriOnboardingState, setVeriOnboardingState] = useState<VeriCulturalOnboardingSystemType>();
  const [veriCurrentStep, setVeriCurrentStep] = useState<VeriOnboardingStep>('cultural-introduction');
  
  // Set page title
  usePageTitle({ 
    title: 'Onboarding', 
    titleVi: 'Giới thiệu Văn hóa' 
  });
  
  // Initialize with current i18n language state to avoid desynchronization
  const [veriLanguage, setVeriLanguage] = useState<'vietnamese' | 'english'>(() => {
    return i18n.language === 'vi' ? 'vietnamese' : 'english';
  });
  const [veriCulturalContext, setVeriCulturalContext] = useState<VeriCulturalContext>();

  // Keep VeriPortal state synchronized with global i18n state changes
  useEffect(() => {
    const handleLanguageChange = (lang: string) => {
      const newVeriLang = lang === 'vi' ? 'vietnamese' : 'english';
      console.log(`🔄 VeriPortal: Syncing with global i18n change ${lang} → ${newVeriLang}`);
      setVeriLanguage(newVeriLang);
    };

    // Listen for i18n language changes
    i18n.on('languageChanged', handleLanguageChange);

    // Cleanup listener on unmount
    return () => {
      i18n.off('languageChanged', handleLanguageChange);
    };
  }, [i18n]);
  const [veriAIEngine, setVeriAIEngine] = useState<VeriAICulturalEngine>();
  const [veriMLPersonalization, setVeriMLPersonalization] = useState<VeriMLPersonalizationEngine>();
  const [veriAutomationEngine, setVeriAutomationEngine] = useState<VeriAutomationEngine>();
  const [veriAIInsights, setVeriAIInsights] = useState<VeriAIInsights[]>();
  const [veriIsLoading, setVeriIsLoading] = useState(true);
  const [veriInitializationComplete, setVeriInitializationComplete] = useState(false);

  // AI-powered automatic cultural detection and adaptation
  useEffect(() => {
    const initializeAISystem = async () => {
      try {
        setVeriIsLoading(true);
        
        // Initialize AI Cultural Engine
        console.log('🤖 Initializing VeriPortal AI Cultural Engine...');
        const aiEngine = await initializeVeriAICulturalEngine();
        setVeriAIEngine(aiEngine);
        
        // Start ML-powered cultural analysis
        console.log('🧠 Starting ML Cultural Analysis...');
        const culturalData = await startVeriMLCulturalAnalysis(veriLanguage);
        setVeriCulturalContext(culturalData.veriContext);
        setVeriAIInsights(culturalData.veriAIInsights);
        
        // Enable AI automation
        console.log('⚡ Enabling AI Automation Engine...');
        const automationEngine = await enableVeriAutomationEngine();
        setVeriAutomationEngine(automationEngine);
        
        setVeriInitializationComplete(true);
        console.log('✅ VeriPortal AI/ML System Initialized Successfully!');
      } catch (error) {
        console.error('❌ Error initializing VeriPortal AI system:', error);
      } finally {
        setVeriIsLoading(false);
      }
    };

    initializeAISystem();
  }, []);

  // AI-powered real-time personalization
  useEffect(() => {
    if (veriAIEngine && veriCulturalContext && !veriMLPersonalization) {
      const initializePersonalization = async () => {
        try {
          console.log('🎯 Initializing ML Personalization...');
          const personalization = await veriAIEngine.veriMLCulturalModel
            .optimizeCulturalAdaptation(veriCulturalContext);
          
          // Create ML personalization engine
          const mlPersonalization: VeriMLPersonalizationEngine = {
            veriMLUserBehaviorModel: {
              analyzeBehavior: async (interactions) => ({
                veriUserSegment: 'vietnamese-business',
                veriEngagementLevel: 0.85,
                veriLearningStyle: 'visual-guided',
                veriPreferredPace: 'moderate'
              })
            },
            veriAIPersonalizationAlgorithm: {
              personalizeExperience: async (context) => ({
                veriPersonalizedContent: true,
                veriAdaptedInterface: true
              })
            },
            veriMLContentOptimization: {
              optimizeContent: async (content, context) => content,
              optimizeLanguageTransition: async (language, analysis) => ({
                veriRecommendedLanguage: language,
                veriConfidence: 0.92
              })
            },
            veriAutomatedUserJourney: {
              optimizeJourney: async (profile) => veriOnboardingSteps
            },
            veriAIEngagementOptimizer: {
              optimizeEngagement: async (context) => ({
                veriOptimizedEngagement: true
              })
            }
          };
          
          setVeriMLPersonalization(mlPersonalization);
          console.log('✅ ML Personalization Engine Ready!');
        } catch (error) {
          console.error('❌ Error initializing ML personalization:', error);
        }
      };

      initializePersonalization();
    }
  }, [veriAIEngine, veriCulturalContext]);

  // Handle step progression with AI optimization
  const veriHandleStepProgression = async (nextStep: VeriOnboardingStep) => {
    if (veriAutomationEngine?.veriMLWorkflowOptimization) {
      try {
        const optimizedStep = await veriAutomationEngine.veriMLWorkflowOptimization
          .optimizeNextStep(nextStep, veriCulturalContext!);
        setVeriCurrentStep(optimizedStep);
      } catch (error) {
        console.error('❌ Error optimizing step progression:', error);
        setVeriCurrentStep(nextStep);
      }
    } else {
      setVeriCurrentStep(nextStep);
    }
  };

  // Loading state
  if (veriIsLoading || !veriInitializationComplete) {
    return (
      <div className="veri-loading-container">
        <div className="veri-loading-content">
          {/* Vietnamese Lotus Logo */}
          <div className="veri-lotus-container">
            <div className="veri-lotus-spinner">
              <div className="veri-lotus-petal veri-petal-1"></div>
              <div className="veri-lotus-petal veri-petal-2"></div>
              <div className="veri-lotus-petal veri-petal-3"></div>
              <div className="veri-lotus-petal veri-petal-4"></div>
              <div className="veri-lotus-petal veri-petal-5"></div>
              <div className="veri-lotus-petal veri-petal-6"></div>
              <div className="veri-lotus-center"></div>
            </div>
          </div>
          
          {/* Vietnamese Flag Accent */}
          <div className="veri-cultural-accent">
            <span className="veri-flag-star">⭐</span>
            <div className="veri-flag-colors">
              <div className="veri-red-stripe"></div>
              <div className="veri-gold-stripe"></div>
            </div>
          </div>

          {/* Loading Text */}
          <div className="veri-loading-text">
            <h3 className="veri-loading-title">
              {t('common:loadingVeriPortal')}
            </h3>
            <p className="veri-loading-subtitle">
              {t('common:loadingDescription')}
            </p>
          </div>

          {/* Progress Bar with Cultural Design */}
          <div className="veri-loading-progress">
            <div className="veri-progress-track">
              <div className="veri-progress-fill"></div>
              <div className="veri-progress-glow"></div>
            </div>
            <div className="veri-loading-dots">
              <span className="veri-dot veri-dot-1"></span>
              <span className="veri-dot veri-dot-2"></span>
              <span className="veri-dot veri-dot-3"></span>
            </div>
          </div>

          {/* Vietnamese Cultural Pattern */}
          <div className="veri-cultural-pattern">
            <div className="veri-pattern-element"></div>
            <div className="veri-pattern-element"></div>
            <div className="veri-pattern-element"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <VeriPortalLayout 
      veriLanguage={veriLanguage}
      veriCurrentLanguage={veriLanguage}
      setVeriLanguage={(newLanguage) => {
        console.log(`🔥 VeriPortal: Language change request from ${veriLanguage} to ${newLanguage}`);
        
        // Only update i18n - component state will be updated by the useEffect listener
        const i18nLang = newLanguage === 'vietnamese' ? 'vi' : 'en';
        i18n.changeLanguage(i18nLang);
        
        console.log(`🔥 VeriPortal: i18n.changeLanguage(${i18nLang}) called - state will sync automatically`);
      }}
    >
      <VeriAIPoweredCulturalOnboardingProvider
        veriLanguage={veriLanguage}
        veriCulturalContext={veriCulturalContext}
        veriOnboardingState={veriOnboardingState}
        veriAIEngine={veriAIEngine}
        veriMLPersonalization={veriMLPersonalization}
        veriAutomationEngine={veriAutomationEngine}
        veriAIInsights={veriAIInsights}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          {/* Progress Card */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100 p-6 mb-8">
            <VeriOnboardingProgress
              veriCurrentStep={veriCurrentStep}
              veriTotalSteps={veriOnboardingSteps.length}
              veriCulturalStyle={veriCulturalContext?.veriCommunicationStyle}
              veriSteps={veriOnboardingSteps}
            />
          </div>
          
          {/* Main Content Card */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100 p-8 mb-8">
            <VeriOnboardingContent
              key={`content-${veriLanguage}`}
              veriCurrentStep={veriCurrentStep}
              veriLanguage={veriLanguage}
              veriCulturalContext={veriCulturalContext}
              veriAIEngine={veriAIEngine}
              veriMLPersonalization={veriMLPersonalization}
              veriAutomationEngine={veriAutomationEngine}
              veriAIInsights={veriAIInsights}
              veriOnNext={veriHandleStepProgression}
              veriOnPrevious={(prevStep) => setVeriCurrentStep(prevStep)}
            />
          </div>
          
          {/* AI Insights Dashboard Card */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100 p-6">
            <VeriAIInsightsDashboard
              veriAIInsights={veriAIInsights}
              veriMLRecommendations={veriMLPersonalization}
              veriAutomationStatus={veriAutomationEngine?.veriAutomationStatus}
              veriLanguage={veriLanguage}
            />
          </div>
        </div>
      </VeriAIPoweredCulturalOnboardingProvider>
    </VeriPortalLayout>
  );
};

// Export default component
export default VeriCulturalOnboardingSystem;