// VeriPortal Regional Adaptation Step - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { useTranslation } from 'react-i18next';
import { VeriOnboardingStep } from '../../types';

interface VeriRegionalAdaptationStepProps {
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriRegionalAdaptationStep: React.FC<VeriRegionalAdaptationStepProps> = ({
  veriOnNext,
  veriOnPrevious
}) => {
  const { t, i18n } = useTranslation(['common', 'veriportal']);

  // Ensure i18n is ready before rendering
  if (!i18n.isInitialized) {
    return (
      <div className="veri-simple-loading">
        <div className="veri-loading-spinner-small"></div>
        <span>Đang tải thông tin khu vực...</span>
      </div>
    );
  }

  return (
    <div>
      <h2>{t('veriportal:regionalAdaptation.title')}</h2>
      <p>{t('veriportal:regionalAdaptation.description')}</p>
      <button onClick={() => veriOnPrevious('business-profile-setup')}>
        {t('common:navigation.back')}
      </button>
      <button onClick={() => veriOnNext('cultural-preferences')}>
        {t('common:navigation.next')}
      </button>
    </div>
  );
};

export default VeriRegionalAdaptationStep;