// VeriPortal Onboarding Progress - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { VeriOnboardingStep } from '../types';
import './VeriOnboardingProgress.css';

interface VeriOnboardingProgressProps {
  veriCurrentStep: VeriOnboardingStep;
  veriTotalSteps: number;
  veriCulturalStyle?: 'formal' | 'balanced' | 'friendly';
  veriSteps: VeriOnboardingStep[];
}

const veriStepLabels: Record<VeriOnboardingStep, { vietnamese: string; english: string }> = {
  'cultural-introduction': {
    vietnamese: 'Giới thiệu Văn hóa',
    english: 'Cultural Introduction'
  },
  'business-profile-setup': {
    vietnamese: 'Thiết lập Hồ sơ',
    english: 'Business Profile'
  },
  'regional-adaptation': {
    vietnamese: 'Tùy chỉnh Vùng miền',
    english: 'Regional Adaptation'
  },
  'cultural-preferences': {
    vietnamese: 'Sở thích Văn hóa',
    english: 'Cultural Preferences'
  },
  'compliance-readiness': {
    vietnamese: 'Sẵn sàng Tuân thủ',
    english: 'Compliance Readiness'
  },
  'completion-summary': {
    vietnamese: 'Tóm tắt Hoàn thành',
    english: 'Completion Summary'
  }
};

const veriStepDescriptions: Record<VeriOnboardingStep, { vietnamese: string; english: string }> = {
  'cultural-introduction': {
    vietnamese: 'Chào mừng đến với VeriPortal - Hiểu văn hóa Việt Nam',
    english: 'Welcome to VeriPortal - Understanding Vietnamese Culture'
  },
  'business-profile-setup': {
    vietnamese: 'Cung cấp thông tin doanh nghiệp của bạn',
    english: 'Provide your business information'
  },
  'regional-adaptation': {
    vietnamese: 'Tùy chỉnh giao diện theo vùng miền',
    english: 'Customize interface for your region'
  },
  'cultural-preferences': {
    vietnamese: 'Thiết lập sở thích văn hóa và giao tiếp',
    english: 'Set cultural and communication preferences'
  },
  'compliance-readiness': {
    vietnamese: 'Đánh giá mức độ sẵn sàng tuân thủ PDPL',
    english: 'Assess PDPL compliance readiness'
  },
  'completion-summary': {
    vietnamese: 'Xem lại và hoàn tất thiết lập',
    english: 'Review and complete setup'
  }
};

export const VeriOnboardingProgress: React.FC<VeriOnboardingProgressProps> = ({
  veriCurrentStep,
  veriTotalSteps,
  veriCulturalStyle = 'balanced',
  veriSteps
}) => {
  const veriCurrentStepIndex = veriSteps.indexOf(veriCurrentStep);
  const veriProgressPercentage = ((veriCurrentStepIndex + 1) / veriTotalSteps) * 100;
  
  // Detect language preference based on current step content
  const veriIsVietnamese = true; // Default to Vietnamese for cultural authenticity

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
          const veriIsPending = index > veriCurrentStepIndex;
          
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
                  {veriStepLabels[step][veriIsVietnamese ? 'vietnamese' : 'english']}
                </div>
                <div className="veri-step-description">
                  {veriStepDescriptions[step][veriIsVietnamese ? 'vietnamese' : 'english']}
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
            {veriStepLabels[veriCurrentStep][veriIsVietnamese ? 'vietnamese' : 'english']}
          </h3>
          <p>
            {veriStepDescriptions[veriCurrentStep][veriIsVietnamese ? 'vietnamese' : 'english']}
          </p>
        </div>
        
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