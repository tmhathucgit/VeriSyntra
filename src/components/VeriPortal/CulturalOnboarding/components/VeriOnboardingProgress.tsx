// VeriPortal Onboarding Progress - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { useTranslation } from 'react-i18next';
import { VeriOnboardingStep } from '../types';
import './VeriOnboardingProgress.css';

interface VeriOnboardingProgressProps {
  veriCurrentStep: VeriOnboardingStep;
  veriTotalSteps: number;
  veriCulturalStyle?: 'formal' | 'balanced' | 'friendly';
  veriSteps: VeriOnboardingStep[];
}

export const VeriOnboardingProgress: React.FC<VeriOnboardingProgressProps> = ({
  veriCurrentStep,
  veriTotalSteps,
  veriCulturalStyle = 'balanced',
  veriSteps
}) => {
  const { t, i18n } = useTranslation(['common', 'veriportal']);
  const veriCurrentStepIndex = veriSteps.indexOf(veriCurrentStep);
  const veriProgressPercentage = ((veriCurrentStepIndex + 1) / veriTotalSteps) * 100;
  
  // Detect language preference based on i18n
  const veriIsVietnamese = i18n.language === 'vi';

  const getStepTitle = (step: VeriOnboardingStep): string => {
    switch (step) {
      case 'cultural-introduction':
        return t('veriportal:culturalIntroduction.title');
      case 'business-profile-setup':
        return t('veriportal:businessContext.title');
      case 'regional-adaptation':
        return t('veriportal:regionalAdaptation.title');
      case 'cultural-preferences':
        return veriIsVietnamese ? 'Sở thích Văn hóa' : 'Cultural Preferences';
      case 'compliance-readiness':
        return veriIsVietnamese ? 'Sẵn sàng Tuân thủ' : 'Compliance Readiness';
      case 'completion-summary':
        return veriIsVietnamese ? 'Tóm tắt Hoàn thành' : 'Completion Summary';
      default:
        return step;
    }
  };

  const getStepDescription = (step: VeriOnboardingStep): string => {
    switch (step) {
      case 'cultural-introduction':
        return t('veriportal:culturalIntroduction.description');
      case 'business-profile-setup':
        return veriIsVietnamese ? 'Cung cấp thông tin doanh nghiệp của bạn' : 'Provide your business information';
      case 'regional-adaptation':
        return t('veriportal:regionalAdaptation.description');
      case 'cultural-preferences':
        return veriIsVietnamese ? 'Thiết lập sở thích văn hóa và giao tiếp' : 'Set cultural and communication preferences';
      case 'compliance-readiness':
        return veriIsVietnamese ? 'Đánh giá mức độ sẵn sàng tuân thủ PDPL' : 'Assess PDPL compliance readiness';
      case 'completion-summary':
        return veriIsVietnamese ? 'Xem lại và hoàn tất thiết lập' : 'Review and complete setup';
      default:
        return step;
    }
  };

  return (
    <div 
      className={`veri-onboarding-progress-container veri-cultural-${veriCulturalStyle}`}
      data-current-step={veriCurrentStep}
      data-progress={veriProgressPercentage}
    >
      {/* Progress Header */}
      <div className="veri-progress-header">
        <div className="veri-progress-title">
          <h2>
            {veriIsVietnamese 
              ? 'Tiến trình Thiết lập VeriPortal' 
              : 'VeriPortal Setup Progress'
            }
          </h2>
          <div className="veri-cultural-indicator">
            <span className="veri-vietnam-flag">🇻🇳</span>
            <span className="veri-cultural-text">
              {veriIsVietnamese 
                ? 'Được tối ưu cho văn hóa Việt Nam' 
                : 'Optimized for Vietnamese Culture'
              }
            </span>
          </div>
        </div>
        
        <div className="veri-progress-summary">
          <span className="veri-step-counter">
            {veriIsVietnamese 
              ? `Bước ${veriCurrentStepIndex + 1} / ${veriTotalSteps}`
              : `Step ${veriCurrentStepIndex + 1} of ${veriTotalSteps}`
            }
          </span>
          <span className="veri-progress-percentage">
            {Math.round(veriProgressPercentage)}%
          </span>
        </div>
      </div>

      {/* Step Actions - Moved above progress bar */}
      <div className="veri-step-actions">
        <div className="veri-cultural-encouragement">
          {veriCulturalStyle === 'formal' && veriIsVietnamese && (
            <span>Kính mời Quý khách tiếp tục quy trình thiết lập</span>
          )}
          {veriCulturalStyle === 'balanced' && veriIsVietnamese && (
            <span>Chúng tôi sẽ hướng dẫn bạn từng bước</span>
          )}
          {veriCulturalStyle === 'friendly' && veriIsVietnamese && (
            <span>Cùng hoàn thành thiết lập nhé!</span>
          )}
          {!veriIsVietnamese && (
            <span>We'll guide you through each step</span>
          )}
        </div>
        
        <div className="veri-estimated-time">
          <span className="veri-clock-icon">⏱️</span>
          <span>
            {veriIsVietnamese 
              ? `Ước tính: ${3 - veriCurrentStepIndex} phút`
              : `Estimated: ${3 - veriCurrentStepIndex} minutes`
            }
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="veri-progress-bar-container">
        <div 
          className="veri-progress-bar"
          style={{ width: `${veriProgressPercentage}%` }}
          data-cultural-region={veriCulturalStyle}
        >
          <div className="veri-progress-shine"></div>
        </div>
        <div className="veri-progress-track"></div>
      </div>

      {/* Step Indicators */}
      <div className="veri-steps-container">
        {veriSteps.map((step, index) => {
          const veriIsCompleted = index < veriCurrentStepIndex;
          const veriIsActive = index === veriCurrentStepIndex;
          
          return (
            <div
              key={step}
              className={`veri-step-indicator ${
                veriIsCompleted ? 'veri-completed' : 
                veriIsActive ? 'veri-active' : 'veri-pending'
              }`}
              data-step={step}
            >
              <div className="veri-step-circle">
                {veriIsCompleted ? (
                  <span className="veri-step-check">✓</span>
                ) : veriIsActive ? (
                  <span className="veri-step-number">{index + 1}</span>
                ) : (
                  <span className="veri-step-number">{index + 1}</span>
                )}
              </div>
              
              <div className="veri-step-content">
                <div className="veri-step-label">
                  {getStepTitle(step)}
                </div>
                <div className="veri-step-description">
                  {getStepDescription(step)}
                </div>
              </div>
              
              {index < veriSteps.length - 1 && (
                <div 
                  className={`veri-step-connector ${
                    veriIsCompleted ? 'veri-connector-completed' : 'veri-connector-pending'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Current Step Highlight */}
      <div className="veri-current-step-highlight">
        <div className="veri-current-step-info">
          <h3>
            {getStepTitle(veriCurrentStep)}
          </h3>
          <p>
            {getStepDescription(veriCurrentStep)}
          </p>
        </div>
      </div>

      {/* Vietnamese Cultural Elements */}
      <div className="veri-cultural-elements">
        <div className="veri-cultural-pattern veri-pattern-north" 
             style={{ opacity: veriCulturalStyle === 'formal' ? 1 : 0.3 }}></div>
        <div className="veri-cultural-pattern veri-pattern-central" 
             style={{ opacity: veriCulturalStyle === 'balanced' ? 1 : 0.3 }}></div>
        <div className="veri-cultural-pattern veri-pattern-south" 
             style={{ opacity: veriCulturalStyle === 'friendly' ? 1 : 0.3 }}></div>
      </div>
    </div>
  );
};

export default VeriOnboardingProgress;