// VeriPDPLSetupWizard Component
// Vietnamese PDPL 2025 Compliance Setup Wizard

import React, { useState, useEffect } from 'react';
import {
  VeriPDPLWizardProps,
  VeriPDPLStep,
  VeriAIComplianceAnalysis,
  VeriLegalBasisData,
  VeriPDPLWizardResult
} from '../types';
import { veriComplianceAIService } from '../services/veriComplianceAIServices';
import { VeriLegalBasisSetupStep } from './VeriLegalBasisSetupStep.tsx';

export const VeriPDPLSetupWizard: React.FC<VeriPDPLWizardProps> = ({
  veriBusinessContext,
  veriLanguage,
  veriOnComplete
}) => {
  const [veriCurrentStep, setVeriCurrentStep] = useState<VeriPDPLStep>('legal-basis-setup');
  const [veriAIAnalysis, setVeriAIAnalysis] = useState<VeriAIComplianceAnalysis | null>(null);
  const [veriStepData, setVeriStepData] = useState<Record<string, any>>({});
  const [veriIsLoading, setVeriIsLoading] = useState(false);

  const veriPDPLWizardContent = {
    vietnamese: {
      veriTitle: "Thiết lập Tuân thủ PDPL 2025",
      veriSubtitle: "Hướng dẫn từng bước để doanh nghiệp tuân thủ Luật Bảo vệ Dữ liệu Cá nhân 2025",
      veriDescription: "AI sẽ phân tích doanh nghiệp của bạn và đưa ra hướng dẫn tuân thủ phù hợp với văn hóa kinh doanh Việt Nam",
      veriSteps: {
        'legal-basis-setup': 'Xác định Cơ sở Pháp lý',
        'data-mapping': 'Lập bản đồ Dữ liệu',
        'consent-management': 'Quản lý Đồng ý',
        'privacy-notice': 'Thông báo Quyền riêng tư',
        'security-measures': 'Biện pháp Bảo mật',
        'incident-response': 'Ứng phó Sự cố',
        'dpo-setup': 'Thiết lập DPO',
        'audit-preparation': 'Chuẩn bị Kiểm tra'
      }
    },
    english: {
      veriTitle: "PDPL 2025 Compliance Setup",
      veriSubtitle: "Step-by-step guidance for Vietnamese businesses to achieve PDPL 2025 compliance",
      veriDescription: "AI will analyze your business and provide compliance guidance tailored to Vietnamese business culture",
      veriSteps: {
        'legal-basis-setup': 'Legal Basis Setup',
        'data-mapping': 'Data Mapping',
        'consent-management': 'Consent Management',
        'privacy-notice': 'Privacy Notice',
        'security-measures': 'Security Measures',
        'incident-response': 'Incident Response',
        'dpo-setup': 'DPO Setup',
        'audit-preparation': 'Audit Preparation'
      }
    }
  };

  // Generate AI analysis on component mount
  useEffect(() => {
    const generateAnalysis = async () => {
      setVeriIsLoading(true);
      try {
        const analysis = await veriComplianceAIService.generateVeriComplianceAnalysis(veriBusinessContext);
        setVeriAIAnalysis(analysis);
      } catch (error) {
        console.error('Failed to generate AI analysis:', error);
      } finally {
        setVeriIsLoading(false);
      }
    };

    generateAnalysis();
  }, [veriBusinessContext]);

  const veriStepOrder: VeriPDPLStep[] = [
    'legal-basis-setup',
    'data-mapping',
    'consent-management',
    'privacy-notice',
    'security-measures',
    'incident-response',
    'dpo-setup',
    'audit-preparation'
  ];

  const isVeriFirstStep = (step: VeriPDPLStep): boolean => {
    return veriStepOrder.indexOf(step) === 0;
  };

  const isVeriLastStep = (step: VeriPDPLStep): boolean => {
    return veriStepOrder.indexOf(step) === veriStepOrder.length - 1;
  };

  const veriGoToPreviousStep = () => {
    const currentIndex = veriStepOrder.indexOf(veriCurrentStep);
    if (currentIndex > 0) {
      setVeriCurrentStep(veriStepOrder[currentIndex - 1]);
    }
  };

  const veriProceedToNextStep = () => {
    const currentIndex = veriStepOrder.indexOf(veriCurrentStep);
    if (currentIndex < veriStepOrder.length - 1) {
      setVeriCurrentStep(veriStepOrder[currentIndex + 1]);
    } else {
      // Wizard completed
      handleWizardComplete();
    }
  };

  const isVeriStepCompleted = (step: VeriPDPLStep): boolean => {
    return !!veriStepData[step];
  };

  const isVeriAIRecommended = (step: VeriPDPLStep): boolean => {
    return veriAIAnalysis?.veriRecommendations?.some(rec => rec.veriRecommendationType === step) || false;
  };

  const isVeriCurrentStepValid = (): boolean => {
    return isVeriStepCompleted(veriCurrentStep);
  };

  const handleStepComplete = (stepKey: VeriPDPLStep, data: any) => {
    setVeriStepData(prev => ({
      ...prev,
      [stepKey]: data
    }));
  };

  const getVeriStepData = (stepKey: VeriPDPLStep) => {
    return veriStepData[stepKey];
  };

  const veriRequestAIGuidance = async (step: VeriPDPLStep) => {
    const currentData = getVeriStepData(step);
    console.log(`AI guidance requested for step: ${step}`, currentData);
    // This would open an AI assistance modal or panel
  };

  const handleWizardComplete = () => {
    const result: VeriPDPLWizardResult = {
      veriLegalBasisData: veriStepData['legal-basis-setup'] as VeriLegalBasisData,
      veriDataMappingData: veriStepData['data-mapping'],
      veriConsentManagementData: veriStepData['consent-management'],
      veriPrivacyNoticeData: veriStepData['privacy-notice'],
      veriSecurityMeasuresData: veriStepData['security-measures'],
      veriIncidentResponseData: veriStepData['incident-response'],
      veriDPOSetupData: veriStepData['dpo-setup'],
      veriAuditPreparationData: veriStepData['audit-preparation'],
      veriComplianceScore: {
        veriOverallScore: 85,
        veriCategoryScores: {},
        veriRiskAssessment: {
          veriOverallRisk: 'medium',
          veriRiskFactors: [],
          veriMitigationRecommendations: []
        },
        veriImprovementRecommendations: [],
        veriConfidenceLevel: 90,
        veriLastCalculated: new Date(),
        veriTrendData: []
      }
    };

    veriOnComplete(result);
  };

  if (veriIsLoading) {
    return (
      <div className="veri-pdpl-wizard-loading">
        <div className="veri-ai-loading-indicator">
          <div className="veri-ai-brain-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="currentColor">
              <path d="M24 4C12.96 4 4 12.96 4 24s8.96 20 20 20 20-8.96 20-20S35.04 4 24 4zm0 36c-8.84 0-16-7.16-16-16S15.16 8 24 8s16 7.16 16 16-7.16 16-16 16z"/>
              <path d="M24 12c-6.63 0-12 5.37-12 12s5.37 12 12 12 12-5.37 12-12-5.37-12-12-12zm0 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/>
            </svg>
          </div>
        </div>
        <p className="veri-ai-loading-text">
          {veriLanguage === 'vietnamese' 
            ? 'AI đang phân tích doanh nghiệp và chuẩn bị wizard...' 
            : 'AI is analyzing your business and preparing the wizard...'}
        </p>
      </div>
    );
  }

  return (
    <div className="veri-pdpl-wizard-container">
      <div className="veri-wizard-header">
        <h2 className="veri-wizard-title">{veriPDPLWizardContent[veriLanguage].veriTitle}</h2>
        <p className="veri-wizard-subtitle">{veriPDPLWizardContent[veriLanguage].veriSubtitle}</p>
        <div className="veri-ai-insight">
          <div className="veri-ai-indicator veri-active">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2C5.58 2 2 5.58 2 10s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/>
              <path d="M10 6c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 6c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
            </svg>
          </div>
          <span className="veri-ai-message">
            {veriPDPLWizardContent[veriLanguage].veriDescription}
          </span>
        </div>
      </div>

      <div className="veri-wizard-steps-navigation">
        {Object.entries(veriPDPLWizardContent[veriLanguage].veriSteps).map(([stepKey, stepTitle]) => (
          <div
            key={stepKey}
            className={`veri-wizard-step-indicator ${
              isVeriStepCompleted(stepKey as VeriPDPLStep) ? 'veri-completed' : ''
            } ${
              veriCurrentStep === stepKey ? 'veri-current' : ''
            } ${
              isVeriAIRecommended(stepKey as VeriPDPLStep) ? 'veri-ai-recommended' : ''
            }`}
          >
            <div className="veri-step-icon">
              {isVeriStepCompleted(stepKey as VeriPDPLStep) ? (
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"/>
                </svg>
              ) : (
                <span className="veri-step-number">{veriStepOrder.indexOf(stepKey as VeriPDPLStep) + 1}</span>
              )}
            </div>
            <span className="veri-step-title">{stepTitle}</span>
            {isVeriAIRecommended(stepKey as VeriPDPLStep) && (
              <div className="veri-ai-recommended-badge">
                <span>{veriLanguage === 'vietnamese' ? 'AI' : 'AI'}</span>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="veri-wizard-step-content">
        {veriCurrentStep === 'legal-basis-setup' && (
          <VeriLegalBasisSetupStep
            veriBusinessContext={veriBusinessContext}
            veriLanguage={veriLanguage}
            veriAIAnalysis={veriAIAnalysis || undefined}
            veriOnComplete={(data) => handleStepComplete('legal-basis-setup', data)}
          />
        )}
        
        {veriCurrentStep === 'data-mapping' && (
          <div className="veri-step-placeholder">
            <h3>{veriPDPLWizardContent[veriLanguage].veriSteps['data-mapping']}</h3>
            <p>
              {veriLanguage === 'vietnamese' 
                ? 'Bước này đang được phát triển và sẽ có sẵn sớm.'
                : 'This step is under development and will be available soon.'}
            </p>
            <button 
              className="veri-wizard-next-button"
              onClick={() => handleStepComplete('data-mapping', { placeholder: true })}
            >
              {veriLanguage === 'vietnamese' ? 'Tiếp tục (Tạm thời)' : 'Continue (Temporary)'}
            </button>
          </div>
        )}

        {/* Placeholder for other steps */}
        {!['legal-basis-setup', 'data-mapping'].includes(veriCurrentStep) && (
          <div className="veri-step-placeholder">
            <h3>{veriPDPLWizardContent[veriLanguage].veriSteps[veriCurrentStep]}</h3>
            <p>
              {veriLanguage === 'vietnamese' 
                ? 'Bước này đang được phát triển và sẽ có sẵn sớm.'
                : 'This step is under development and will be available soon.'}
            </p>
            <button 
              className="veri-wizard-next-button"
              onClick={() => handleStepComplete(veriCurrentStep, { placeholder: true })}
            >
              {veriLanguage === 'vietnamese' ? 'Tiếp tục (Tạm thời)' : 'Continue (Temporary)'}
            </button>
          </div>
        )}
      </div>

      <div className="veri-wizard-actions">
        <button
          className="veri-wizard-back-button"
          disabled={isVeriFirstStep(veriCurrentStep)}
          onClick={veriGoToPreviousStep}
        >
          {veriLanguage === 'vietnamese' ? 'Quay lại' : 'Back'}
        </button>
        
        <button
          className="veri-ai-help-button"
          onClick={() => veriRequestAIGuidance(veriCurrentStep)}
        >
          {veriLanguage === 'vietnamese' ? 'Trợ giúp AI' : 'AI Assistance'}
        </button>
        
        <button
          className="veri-wizard-next-button"
          disabled={!isVeriCurrentStepValid()}
          onClick={veriProceedToNextStep}
        >
          {isVeriLastStep(veriCurrentStep) 
            ? (veriLanguage === 'vietnamese' ? 'Hoàn thành' : 'Complete')
            : (veriLanguage === 'vietnamese' ? 'Tiếp tục' : 'Continue')
          }
        </button>
      </div>
    </div>
  );
};