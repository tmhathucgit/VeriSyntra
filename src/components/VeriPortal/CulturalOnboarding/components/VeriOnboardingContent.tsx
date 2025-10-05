// VeriPortal Onboarding Content - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import {
  VeriOnboardingStep,
  VeriCulturalContext,
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine,
  VeriAIInsights
} from '../types';
import {
  VeriCulturalIntroductionStep,
  VeriBusinessProfileSetupStep,
  VeriRegionalAdaptationStep,
  VeriCulturalPreferencesStep,
  VeriComplianceReadinessStep,
  VeriCompletionSummaryStep
} from './steps';
import './VeriOnboardingContent.css';

interface VeriOnboardingContentProps {
  veriCurrentStep: VeriOnboardingStep;
  veriLanguage: 'vietnamese' | 'english';
  veriCulturalContext?: VeriCulturalContext;
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
  veriAIInsights?: VeriAIInsights[];
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriOnboardingContent: React.FC<VeriOnboardingContentProps> = ({
  veriCurrentStep,
  veriLanguage,
  veriCulturalContext,
  veriAIEngine,
  veriMLPersonalization,
  veriAutomationEngine,
  veriAIInsights,
  veriOnNext,
  veriOnPrevious
}) => {
  // Debug language changes
  console.log(`📄 VeriOnboardingContent: Current language is ${veriLanguage}`);
  const renderCurrentStep = () => {
    const commonProps = {
      veriLanguage,
      veriCulturalContext,
      veriAIEngine,
      veriMLPersonalization,
      veriAutomationEngine,
      veriAIInsights,
      veriOnNext,
      veriOnPrevious
    };

    switch (veriCurrentStep) {
      case 'cultural-introduction':
        return <VeriCulturalIntroductionStep {...commonProps} />;
      case 'business-profile-setup':
        return <VeriBusinessProfileSetupStep {...commonProps} />;
      case 'regional-adaptation':
        return <VeriRegionalAdaptationStep {...commonProps} />;
      case 'cultural-preferences':
        return <VeriCulturalPreferencesStep {...commonProps} />;
      case 'compliance-readiness':
        return <VeriComplianceReadinessStep {...commonProps} />;
      case 'completion-summary':
        return <VeriCompletionSummaryStep {...commonProps} />;
      default:
        return <VeriCulturalIntroductionStep {...commonProps} />;
    }
  };

  return (
    <div className="veri-onboarding-content-container" data-step={veriCurrentStep}>
      {renderCurrentStep()}
    </div>
  );
};

export default VeriOnboardingContent;