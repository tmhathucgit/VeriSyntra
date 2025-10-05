// VeriPortal_02_ComplianceWizards Main Component
// Vietnamese PDPL 2025 Compliance Wizards System

import React, { useState, useEffect, useContext, createContext } from 'react';
import {
  VeriComplianceWizardSystem as VeriComplianceWizardSystemType,
  VeriWizardType,
  VeriBusinessContext,
  VeriComplianceWizardProps,
  VeriWizardContextType,
  VeriAIWizardEngine,
  VeriAIComplianceAnalysis
} from '../types';
import { veriComplianceAIService } from '../services/veriComplianceAIServices';
import { VeriPDPLSetupWizard } from './VeriPDPLSetupWizard';
import { VeriLanguageSwitcher } from '../../CulturalOnboarding/components/VeriLanguageSwitcher';
import { VeriSyntraBanner } from '../../../shared/VeriSyntraBanner';
import '../styles/VeriComplianceWizards.css';

// Vietnamese Compliance Wizard Context
const VeriWizardContext = createContext<VeriWizardContextType | null>(null);

// Context Provider Component
export const VeriComplianceWizardProvider: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext: VeriBusinessContext | null;
  veriAIEngine: VeriAIWizardEngine | null;
  children: React.ReactNode;
}> = ({ 
  veriLanguage, 
  veriBusinessContext, 
  veriAIEngine, 
  children 
}) => {
  const [veriWizardState, setVeriWizardState] = useState<VeriComplianceWizardSystemType | null>(null);
  const [veriCurrentWizard, setVeriCurrentWizard] = useState<VeriWizardType>('pdpl-2025-setup');
  const [veriCurrentLanguage, setVeriCurrentLanguage] = useState<'vietnamese' | 'english'>(veriLanguage);
  const [veriCurrentBusinessContext, setVeriCurrentBusinessContext] = useState<VeriBusinessContext | null>(veriBusinessContext);
  const [veriCurrentAIEngine, setVeriCurrentAIEngine] = useState<VeriAIWizardEngine | null>(veriAIEngine);

  const contextValue: VeriWizardContextType = {
    veriWizardState,
    veriSetWizardState: setVeriWizardState,
    veriCurrentWizard,
    veriSetCurrentWizard: setVeriCurrentWizard,
    veriLanguage: veriCurrentLanguage,
    veriSetLanguage: setVeriCurrentLanguage,
    veriBusinessContext: veriCurrentBusinessContext,
    veriSetBusinessContext: setVeriCurrentBusinessContext,
    veriAIEngine: veriCurrentAIEngine,
    veriSetAIEngine: setVeriCurrentAIEngine
  };

  return (
    <VeriWizardContext.Provider value={contextValue}>
      {children}
    </VeriWizardContext.Provider>
  );
};

// Hook to use Wizard Context
export const useVeriWizardContext = (): VeriWizardContextType => {
  const context = useContext(VeriWizardContext);
  if (!context) {
    throw new Error('useVeriWizardContext must be used within VeriComplianceWizardProvider');
  }
  return context;
};

// Wizard Layout Component
const VeriWizardLayout: React.FC<{
  veriCulturalStyle?: string;
  children: React.ReactNode;
}> = ({ veriCulturalStyle, children }) => {
  return (
    <div className={`veri-wizard-layout ${veriCulturalStyle ? `veri-cultural-${veriCulturalStyle}` : ''}`}>
      {children}
    </div>
  );
};

// Wizard Selector Component
const VeriWizardSelector: React.FC<{
  veriAvailableWizards: VeriWizardType[];
  veriCurrentWizard: VeriWizardType;
  veriOnSelectWizard: (wizard: VeriWizardType) => void;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriAvailableWizards, veriCurrentWizard, veriOnSelectWizard, veriLanguage }) => {
  const veriWizardNames = {
    vietnamese: {
      'pdpl-2025-setup': 'Thiết lập PDPL 2025',
      'mps-integration': 'Tích hợp với Bộ Công an',
      'cultural-compliance': 'Tuân thủ Văn hóa',
      'risk-management': 'Quản lý Rủi ro',
      'data-mapping': 'Lập bản đồ Dữ liệu',
      'policy-generation': 'Tạo Chính sách',
      'audit-preparation': 'Chuẩn bị Kiểm tra',
      'cross-border-transfer': 'Chuyển giao Xuyên biên giới'
    },
    english: {
      'pdpl-2025-setup': 'PDPL 2025 Setup',
      'mps-integration': 'MPS Integration',
      'cultural-compliance': 'Cultural Compliance',
      'risk-management': 'Risk Management',
      'data-mapping': 'Data Mapping',
      'policy-generation': 'Policy Generation',
      'audit-preparation': 'Audit Preparation',
      'cross-border-transfer': 'Cross-border Transfer'
    }
  };

  return (
    <div className="veri-wizard-selector">
      <div className="veri-wizard-selector-header">
        <h3 className="veri-wizard-selector-title">
          {veriLanguage === 'vietnamese' ? 'Chọn Wizard Tuân thủ' : 'Select Compliance Wizard'}
        </h3>
      </div>
      <div className="veri-wizard-options">
        {veriAvailableWizards.map(wizard => (
          <button
            key={wizard}
            className={`veri-wizard-option ${veriCurrentWizard === wizard ? 'veri-active' : ''}`}
            onClick={() => veriOnSelectWizard(wizard)}
          >
            <div className="veri-wizard-option-content">
              <span className="veri-wizard-option-name">
                {veriWizardNames[veriLanguage][wizard]}
              </span>
              {veriCurrentWizard === wizard && (
                <span className="veri-wizard-active-indicator">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"/>
                  </svg>
                </span>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

// Wizard Progress Component
const VeriWizardProgress: React.FC<{
  veriCurrentStep?: string;
  veriTotalSteps?: number;
  veriComplianceScore?: any;
}> = ({ veriCurrentStep, veriTotalSteps = 8, veriComplianceScore }) => {
  const { veriLanguage } = useVeriWizardContext();

  const currentStepIndex = veriCurrentStep ? ['legal-basis-setup', 'data-mapping', 'consent-management', 'privacy-notice', 'security-measures', 'incident-response', 'dpo-setup', 'audit-preparation'].indexOf(veriCurrentStep) + 1 : 0;
  const progressPercentage = (currentStepIndex / veriTotalSteps) * 100;

  return (
    <div className="veri-wizard-progress">
      <div className="veri-wizard-progress-header">
        <h4 className="veri-wizard-progress-title">
          {veriLanguage === 'vietnamese' ? 'Tiến độ Wizard' : 'Wizard Progress'}
        </h4>
        <div className="veri-wizard-progress-stats">
          <span className="veri-wizard-step-counter">
            {currentStepIndex} / {veriTotalSteps}
          </span>
          {veriComplianceScore && (
            <span className="veri-compliance-score">
              {veriLanguage === 'vietnamese' ? 'Điểm: ' : 'Score: '}
              {veriComplianceScore.veriOverallScore || 0}%
            </span>
          )}
        </div>
      </div>
      <div className="veri-progress-bar">
        <div 
          className="veri-progress-bar-fill"
          style={{ width: `${progressPercentage}%` }}
        />
      </div>
    </div>
  );
};

// Wizard Content Component
const VeriWizardContent: React.FC<{
  veriWizardType: VeriWizardType;
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext: VeriBusinessContext | null;
  veriAIRecommendations?: any[];
}> = ({ veriWizardType, veriLanguage, veriBusinessContext, veriAIRecommendations }) => {
  if (!veriBusinessContext) {
    return (
      <div className="veri-wizard-content-error">
        <p>{veriLanguage === 'vietnamese' ? 'Cần thông tin doanh nghiệp để bắt đầu' : 'Business context required to start'}</p>
      </div>
    );
  }

  switch (veriWizardType) {
    case 'pdpl-2025-setup':
      return (
        <VeriPDPLSetupWizard
          veriBusinessContext={veriBusinessContext}
          veriLanguage={veriLanguage}
          veriOnComplete={(result) => {
            console.log('PDPL Wizard completed:', result);
          }}
        />
      );
    
    default:
      return (
        <div className="veri-wizard-content-placeholder">
          <div className="veri-wizard-placeholder-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="currentColor">
              <path d="M24 4C12.95 4 4 12.95 4 24s8.95 20 20 20 20-8.95 20-20S35.05 4 24 4zm0 36c-8.82 0-16-7.18-16-16S15.18 8 24 8s16 7.18 16 16-7.18 16-16 16z"/>
              <path d="M22 22h4v12h-4zm0-8h4v4h-4z"/>
            </svg>
          </div>
          <h3 className="veri-wizard-placeholder-title">
            {veriLanguage === 'vietnamese' ? 'Wizard Đang Phát triển' : 'Wizard Under Development'}
          </h3>
          <p className="veri-wizard-placeholder-message">
            {veriLanguage === 'vietnamese' 
              ? 'Wizard này đang được phát triển và sẽ có sẵn sớm.' 
              : 'This wizard is under development and will be available soon.'}
          </p>
        </div>
      );
  }
};

// Main Vietnamese Compliance Wizard System Component
export const VeriComplianceWizardSystem: React.FC<VeriComplianceWizardProps> = ({
  veriBusinessContext: initialBusinessContext,
  veriLanguage: initialLanguage = 'vietnamese',
  veriOnComplete,
  veriOnStepChange,
  veriCulturalStyle
}) => {
  const [veriWizardState, setVeriWizardState] = useState<VeriComplianceWizardSystemType | null>(null);
  const [veriCurrentWizard, setVeriCurrentWizard] = useState<VeriWizardType>('pdpl-2025-setup');
  const [veriLanguage, setVeriLanguage] = useState<'vietnamese' | 'english'>(initialLanguage);
  const [veriBusinessContext, setVeriBusinessContext] = useState<VeriBusinessContext | null>(initialBusinessContext || null);
  const [veriAIEngine, setVeriAIEngine] = useState<VeriAIWizardEngine | null>(null);
  const [veriAIAnalysis, setVeriAIAnalysis] = useState<VeriAIComplianceAnalysis | null>(null);
  const [veriIsLoading, setVeriIsLoading] = useState(false);

  // Initialize default business context if not provided
  useEffect(() => {
    if (!veriBusinessContext) {
      const defaultContext: VeriBusinessContext = {
        veriBusinessId: `veri_business_${Date.now()}`,
        veriIndustryType: {
          veriIndustryCode: 'general',
          veriIndustryName: 'General Business',
          veriIndustryNameVi: 'Doanh nghiệp Tổng quát',
          veriRegulatoryLevel: 'medium',
          veriSpecialRequirements: []
        },
        veriDataProcessingLevel: 'moderate',
        veriRegionalLocation: 'south',
        veriComplianceMaturity: 'beginner',
        veriRegulatoryHistory: {
          veriPreviousCompliance: false,
          veriComplianceFrameworks: [],
          veriAuditHistory: [],
          veriIncidentHistory: []
        },
        veriStakeholderRoles: [],
        veriCulturalPreferences: {
          veriCommunicationStyle: 'consultative',
          veriDecisionMakingStyle: 'collaborative',
          veriInformationDensity: 'moderate',
          veriValidationLevel: 'standard'
        }
      };
      setVeriBusinessContext(defaultContext);
    }
  }, [veriBusinessContext]);

  // Generate AI analysis when business context is available
  useEffect(() => {
    if (veriBusinessContext && !veriAIAnalysis) {
      setVeriIsLoading(true);
      veriComplianceAIService.generateVeriComplianceAnalysis(veriBusinessContext)
        .then(analysis => {
          setVeriAIAnalysis(analysis);
          setVeriIsLoading(false);
        })
        .catch(error => {
          console.error('Failed to generate AI analysis:', error);
          setVeriIsLoading(false);
        });
    }
  }, [veriBusinessContext, veriAIAnalysis]);

  // Initialize AI Engine
  useEffect(() => {
    if (!veriAIEngine) {
      const defaultAIEngine: VeriAIWizardEngine = {
        veriEngineId: 'veri_ai_engine_v1',
        veriEngineVersion: '1.0.0',
        veriCapabilities: ['business_analysis', 'legal_recommendations', 'cultural_intelligence'],
        veriLanguages: ['vietnamese', 'english'],
        veriCulturalModels: ['north_vietnam', 'central_vietnam', 'south_vietnam'],
        veriAnalysisTypes: ['compliance', 'risk', 'cultural']
      };
      setVeriAIEngine(defaultAIEngine);
    }
  }, [veriAIEngine]);

  const getVeriAvailableWizards = (businessContext: VeriBusinessContext | null): VeriWizardType[] => {
    const allWizards: VeriWizardType[] = [
      'pdpl-2025-setup',
      'mps-integration',
      'cultural-compliance',
      'risk-management',
      'data-mapping',
      'policy-generation',
      'audit-preparation',
      'cross-border-transfer'
    ];

    // For now, return all wizards (can be filtered based on business context later)
    return allWizards;
  };

  const handleVeriLanguageChange = (language: 'vietnamese' | 'english') => {
    setVeriLanguage(language);
  };

  const handleVeriWizardSelection = (wizard: VeriWizardType) => {
    setVeriCurrentWizard(wizard);
    if (veriOnStepChange) {
      veriOnStepChange(`wizard-${wizard}`);
    }
  };

  if (veriIsLoading) {
    return (
      <div className="veri-wizard-loading">
        <div className="veri-wizard-loading-spinner">
          <div className="veri-lotus-spinner">
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
          </div>
        </div>
        <p className="veri-wizard-loading-text">
          {veriLanguage === 'vietnamese' 
            ? 'AI đang phân tích doanh nghiệp của bạn...' 
            : 'AI is analyzing your business...'}
        </p>
      </div>
    );
  }

  return (
    <VeriComplianceWizardProvider
      veriLanguage={veriLanguage}
      veriBusinessContext={veriBusinessContext}
      veriAIEngine={veriAIEngine}
    >
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-green-50" style={{
        background: 'linear-gradient(135deg, #f0f4f0 0%, #f1f6fb 25%, #f0f4f0 50%, #f1f6fb 75%, #f0f4f0 100%)'
      }}>
        <VeriSyntraBanner
          variant="portal"
          customTitle="VeriPortal"
          customSubtitle={veriLanguage === 'vietnamese' ? 'Hệ thống Wizard Tuân thủ PDPL 2025' : 'PDPL 2025 Compliance Wizards'}
          currentLanguage={veriLanguage === 'vietnamese' ? 'vi' : 'en'}
          onLanguageChange={(lang) => handleVeriLanguageChange(lang === 'vi' ? 'vietnamese' : 'english')}
          showConnectionStatus={true}
          showLanguageToggle={true}
        />
        
        <VeriWizardLayout veriCulturalStyle={veriBusinessContext?.veriRegionalLocation || veriCulturalStyle}>
          <div className="veri-wizard-header">
            <div className="veri-wizard-header-content">
              <h1 className="veri-wizard-title">
                {veriLanguage === 'vietnamese' ? 'Hệ thống Wizard Tuân thủ PDPL 2025' : 'PDPL 2025 Compliance Wizards'}
              </h1>
              <p className="veri-wizard-subtitle">
                {veriLanguage === 'vietnamese' 
                  ? 'Hướng dẫn từng bước với AI để đạt tuân thủ hoàn toàn'
                  : 'Step-by-step AI guidance for complete compliance'}
              </p>
            </div>
          </div>

        <div className="veri-wizard-main-content">
          <div className="veri-wizard-sidebar">
            <VeriWizardSelector
              veriAvailableWizards={getVeriAvailableWizards(veriBusinessContext)}
              veriCurrentWizard={veriCurrentWizard}
              veriOnSelectWizard={handleVeriWizardSelection}
              veriLanguage={veriLanguage}
            />
            
            <VeriWizardProgress
              veriCurrentStep={veriWizardState?.veriProgressState?.veriCurrentStep}
              veriTotalSteps={veriWizardState?.veriComplianceSteps?.length}
              veriComplianceScore={veriWizardState?.veriComplianceScore}
            />
          </div>

          <div className="veri-wizard-content">
            <VeriWizardContent
              veriWizardType={veriCurrentWizard}
              veriLanguage={veriLanguage}
              veriBusinessContext={veriBusinessContext}
              veriAIRecommendations={veriAIAnalysis?.veriRecommendations}
            />
          </div>
        </div>
      </VeriWizardLayout>
      </div>
    </VeriComplianceWizardProvider>
  );
};