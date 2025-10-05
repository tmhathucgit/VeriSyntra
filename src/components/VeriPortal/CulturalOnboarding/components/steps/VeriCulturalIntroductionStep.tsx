// VeriPortal Cultural Introduction Step - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  VeriOnboardingStep,
  VeriCulturalContext,
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine,
  VeriAIInsights
} from '../../types';
import './VeriCulturalIntroductionStep.css';

interface VeriCulturalIntroductionStepProps {
  veriLanguage: 'vietnamese' | 'english';
  veriCulturalContext?: VeriCulturalContext;
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
  veriAIInsights?: VeriAIInsights[];
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriCulturalIntroductionStep: React.FC<VeriCulturalIntroductionStepProps> = ({
  veriLanguage,
  veriCulturalContext,
  veriOnNext
}) => {
  const { t, i18n } = useTranslation('veriportal');

  console.log(`🏁 VeriCulturalIntroductionStep: Rendering with language ${veriLanguage} at ${new Date().toLocaleTimeString()}`);
  
  // Update i18n language when veriLanguage prop changes
  useEffect(() => {
    const newLang = veriLanguage === 'vietnamese' ? 'vi' : 'en';
    console.log(`📝 VeriCulturalIntroductionStep: Language changing to ${veriLanguage} (i18n: ${newLang})`);
    
    if (i18n.language !== newLang) {
      i18n.changeLanguage(newLang);
      console.log(`🌐 i18n language changed from ${i18n.language} to ${newLang}`);
    }
  }, [veriLanguage, i18n]);

  const veriProceedToNextStep = () => {
    veriOnNext('business-profile-setup');
  };

  return (
    <div className="veri-cultural-introduction-container">
      <div className="veri-cultural-welcome-header">
        <div className="veri-vietnam-emblem">
          <span className="veri-flag">🇻🇳</span>
        </div>
        <h1 className="veri-title">{t('culturalIntroduction.title')}</h1>
        <p className="veri-subtitle">{t('culturalIntroduction.subtitle')}</p>
      </div>
      
      <div className="veri-cultural-promise">
        <p className="veri-description">
          {t('culturalIntroduction.description')}
        </p>
        <div className="veri-highlight">
          {t('culturalIntroduction.culturalPromise')}
        </div>
      </div>
      
      <div className="veri-cultural-features-list">
        <div className="veri-feature-item" data-icon="🇻🇳">
          <div className="veri-feature-icon">🇻🇳</div>
          <div className="veri-feature-content">
            {veriLanguage === 'vietnamese' 
              ? 'Giao diện tiếng Việt tối ưu với văn hóa địa phương'
              : 'Vietnamese-optimized interface with local cultural adaptation'
            }
          </div>
        </div>
        <div className="veri-feature-item" data-icon="🏢">
          <div className="veri-feature-icon">🏢</div>
          <div className="veri-feature-content">
            {veriLanguage === 'vietnamese'
              ? 'Hiểu biết sâu về phân cấp và quy trình kinh doanh Việt Nam'
              : 'Deep understanding of Vietnamese business hierarchy and processes'
            }
          </div>
        </div>
        <div className="veri-feature-item" data-icon="⚖️">
          <div className="veri-feature-icon">⚖️</div>
          <div className="veri-feature-content">
            {veriLanguage === 'vietnamese'
              ? 'Tuân thủ PDPL 2025 với bối cảnh kinh doanh Việt Nam'
              : 'PDPL 2025 compliance with Vietnamese business context'
            }
          </div>
        </div>
      </div>
      
      {veriCulturalContext && (
        <div className="veri-cultural-detection">
          <h3>
            {veriLanguage === 'vietnamese' 
              ? 'AI đã phát hiện văn hóa của bạn' 
              : 'AI Detected Your Culture'
            }
          </h3>
          <div className="veri-detection-result">
            <div className="veri-region-badge" data-region={veriCulturalContext.veriRegion}>
              {veriCulturalContext.veriRegion === 'north' && '🏔️ Miền Bắc'}
              {veriCulturalContext.veriRegion === 'central' && '🏖️ Miền Trung'}
              {veriCulturalContext.veriRegion === 'south' && '🏙️ Miền Nam'}
            </div>
            <div className="veri-business-style">
              {veriLanguage === 'vietnamese' 
                ? `Phong cách: ${veriCulturalContext.veriCommunicationStyle === 'formal' ? 'Trang trọng' : 
                    veriCulturalContext.veriCommunicationStyle === 'balanced' ? 'Cân bằng' : 'Thân thiện'}`
                : `Style: ${veriCulturalContext.veriCommunicationStyle}`
              }
            </div>
          </div>
        </div>
      )}
      
      <div className="veri-action-section">
        <button 
          className="veri-primary-action-button"
          onClick={veriProceedToNextStep}
        >
          <span className="veri-button-icon">➡️</span>
          {t('culturalIntroduction.nextAction')}
        </button>
      </div>
    </div>
  );
};

export default VeriCulturalIntroductionStep;