// VeriPortal Document Generation System - Main Component
// Vietnamese Legal Document Generation with AI-Powered Cultural Intelligence

import React, { useState, useEffect, useContext, createContext } from 'react';
import { usePageTitle } from '../../../../hooks/usePageTitle';
import {
  VeriDocumentGenerationSystem as VeriDocumentGenerationSystemType,
  VeriDocumentType,
  VeriBusinessProfile,
  VeriDocumentGenerationProps,
  VeriDocumentContextType,
  VeriAIDocumentGenerator,
  VeriGeneratedDocument,
  VeriAIDocumentAnalysis,
  VeriDocumentGenerationStatus
} from '../types';
import { veriDocumentAIService } from '../services/veriDocumentAIServices';
import { VeriSyntraBanner } from '../../../shared/VeriSyntraBanner';
import '../styles/VeriDocumentGeneration.css';

// Vietnamese Document Generation Context
const VeriDocumentContext = createContext<VeriDocumentContextType | null>(null);

// Context Provider Component
export const VeriDocumentGenerationProvider: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext: VeriBusinessProfile | null;
  veriAIGenerator: VeriAIDocumentGenerator | null;
  children: React.ReactNode;
}> = ({ 
  veriLanguage, 
  veriBusinessContext, 
  veriAIGenerator, 
  children 
}) => {
  const [veriDocumentState, setVeriDocumentState] = useState<VeriDocumentGenerationSystemType | null>(null);
  const [veriSelectedDocuments, setVeriSelectedDocuments] = useState<VeriDocumentType[]>([]);
  const [veriCurrentLanguage, setVeriCurrentLanguage] = useState<'vietnamese' | 'english'>(veriLanguage);
  const [veriCurrentBusinessContext, setVeriCurrentBusinessContext] = useState<VeriBusinessProfile | null>(veriBusinessContext);
  const [veriCurrentAIGenerator, setVeriCurrentAIGenerator] = useState<VeriAIDocumentGenerator | null>(veriAIGenerator);

  const contextValue: VeriDocumentContextType = {
    veriDocumentState,
    veriSetDocumentState: setVeriDocumentState,
    veriSelectedDocuments,
    veriSetSelectedDocuments: setVeriSelectedDocuments,
    veriLanguage: veriCurrentLanguage,
    veriSetLanguage: setVeriCurrentLanguage,
    veriBusinessContext: veriCurrentBusinessContext,
    veriSetBusinessContext: setVeriCurrentBusinessContext,
    veriAIGenerator: veriCurrentAIGenerator,
    veriSetAIGenerator: setVeriCurrentAIGenerator
  };

  return (
    <VeriDocumentContext.Provider value={contextValue}>
      {children}
    </VeriDocumentContext.Provider>
  );
};

// Hook to use Document Context
export const useVeriDocumentContext = (): VeriDocumentContextType => {
  const context = useContext(VeriDocumentContext);
  if (!context) {
    throw new Error('useVeriDocumentContext must be used within VeriDocumentGenerationProvider');
  }
  return context;
};

// Document Type Selector Component
const VeriDocumentTypeSelector: React.FC<{
  veriAvailableDocuments: VeriDocumentType[];
  veriSelectedDocuments: VeriDocumentType[];
  veriOnDocumentSelection: (documents: VeriDocumentType[]) => void;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriAvailableDocuments, veriSelectedDocuments, veriOnDocumentSelection, veriLanguage }) => {
  const veriDocumentNames = {
    vietnamese: {
      'privacy-policy': 'Chính sách Bảo vệ Dữ liệu Cá nhân',
      'privacy-notice': 'Thông báo Bảo mật',
      'consent-forms': 'Biểu mẫu Đồng ý',
      'data-processing-agreement': 'Thỏa thuận Xử lý Dữ liệu',
      'data-subject-rights-procedure': 'Quy trình Quyền Chủ thể Dữ liệu',
      'security-incident-response-plan': 'Kế hoạch Ứng phó Sự cố Bảo mật',
      'data-retention-policy': 'Chính sách Lưu trữ Dữ liệu',
      'cross-border-transfer-agreement': 'Thỏa thuận Chuyển giao Xuyên biên giới',
      'dpo-appointment-letter': 'Thư Bổ nhiệm DPO',
      'compliance-audit-checklist': 'Danh sách Kiểm tra Tuân thủ',
      'employee-privacy-training-materials': 'Tài liệu Đào tạo Bảo mật Nhân viên',
      'vendor-privacy-assessment': 'Đánh giá Bảo mật Nhà cung cấp'
    },
    english: {
      'privacy-policy': 'Privacy Policy',
      'privacy-notice': 'Privacy Notice',
      'consent-forms': 'Consent Forms',
      'data-processing-agreement': 'Data Processing Agreement',
      'data-subject-rights-procedure': 'Data Subject Rights Procedure',
      'security-incident-response-plan': 'Security Incident Response Plan',
      'data-retention-policy': 'Data Retention Policy',
      'cross-border-transfer-agreement': 'Cross-border Transfer Agreement',
      'dpo-appointment-letter': 'DPO Appointment Letter',
      'compliance-audit-checklist': 'Compliance Audit Checklist',
      'employee-privacy-training-materials': 'Employee Privacy Training Materials',
      'vendor-privacy-assessment': 'Vendor Privacy Assessment'
    }
  };

  const handleDocumentToggle = (document: VeriDocumentType) => {
    const isSelected = veriSelectedDocuments.includes(document);
    if (isSelected) {
      veriOnDocumentSelection(veriSelectedDocuments.filter(d => d !== document));
    } else {
      veriOnDocumentSelection([...veriSelectedDocuments, document]);
    }
  };

  return (
    <div className="veri-document-type-selector">
      <div className="veri-document-selector-header">
        <h3 className="veri-document-selector-title">
          {veriLanguage === 'vietnamese' ? 'Chọn Tài liệu cần Tạo' : 'Select Documents to Generate'}
        </h3>
        <p className="veri-document-selector-subtitle">
          {veriLanguage === 'vietnamese' ? 
            'AI sẽ tạo tài liệu tuân thủ PDPL 2025 cho doanh nghiệp của bạn' : 
            'AI will generate PDPL 2025 compliant documents for your business'}
        </p>
      </div>
      
      <div className="veri-document-grid">
        {veriAvailableDocuments.map(document => (
          <div
            key={document}
            className={`veri-document-card ${veriSelectedDocuments.includes(document) ? 'veri-selected' : ''}`}
            onClick={() => handleDocumentToggle(document)}
          >
            <div className="veri-document-card-header">
              <div className="veri-document-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14 2H6C4.9 2 4 2.9 4 4v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6z"/>
                  <path d="M14 2v6h6"/>
                </svg>
              </div>
              <div className="veri-document-checkbox">
                {veriSelectedDocuments.includes(document) && (
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"/>
                  </svg>
                )}
              </div>
            </div>
            
            <div className="veri-document-card-content">
              <h4 className="veri-document-title">
                {veriDocumentNames[veriLanguage][document]}
              </h4>
              
              <div className="veri-document-features">
                <span className="veri-feature-badge">
                  {veriLanguage === 'vietnamese' ? 'AI Tạo tự động' : 'AI Generated'}
                </span>
                <span className="veri-feature-badge">
                  {veriLanguage === 'vietnamese' ? 'PDPL 2025' : 'PDPL 2025'}
                </span>
                <span className="veri-feature-badge">
                  {veriLanguage === 'vietnamese' ? 'Văn hóa VN' : 'VN Culture'}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="veri-document-selection-summary">
        <span className="veri-selection-count">
          {veriLanguage === 'vietnamese' ? 
            `Đã chọn ${veriSelectedDocuments.length} tài liệu` :
            `Selected ${veriSelectedDocuments.length} documents`
          }
        </span>
      </div>
    </div>
  );
};

// Document Generation Progress Component
const VeriDocumentGenerationProgress: React.FC<{
  veriSelectedDocuments: VeriDocumentType[];
  veriGenerationStatus?: VeriDocumentGenerationStatus;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriSelectedDocuments, veriGenerationStatus, veriLanguage }) => {
  if (!veriGenerationStatus || veriSelectedDocuments.length === 0) {
    return null;
  }

  return (
    <div className="veri-generation-progress">
      <div className="veri-progress-header">
        <h4 className="veri-progress-title">
          {veriLanguage === 'vietnamese' ? 'Tiến trình Tạo Tài liệu' : 'Document Generation Progress'}
        </h4>
        <span className="veri-progress-percentage">{veriGenerationStatus.veriProgress}%</span>
      </div>
      
      <div className="veri-progress-bar">
        <div 
          className="veri-progress-fill"
          style={{ width: `${veriGenerationStatus.veriProgress}%` }}
        ></div>
      </div>
      
      <div className="veri-progress-details">
        <p className="veri-current-step">{veriGenerationStatus.veriCurrentStep}</p>
        
        {veriGenerationStatus.veriEstimatedTimeRemaining && (
          <p className="veri-estimated-time">
            {veriLanguage === 'vietnamese' ? 
              `Thời gian còn lại: ~${veriGenerationStatus.veriEstimatedTimeRemaining}s` :
              `Estimated time: ~${veriGenerationStatus.veriEstimatedTimeRemaining}s`
            }
          </p>
        )}
      </div>

      {veriGenerationStatus.veriStatus === 'generating' && (
        <div className="veri-ai-working-indicator">
          <div className="veri-lotus-spinner">
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
            <div className="veri-lotus-petal"></div>
          </div>
          <span className="veri-ai-status-text">
            {veriLanguage === 'vietnamese' ? 
              'AI đang tạo tài liệu với trí tuệ văn hóa Việt Nam...' :
              'AI generating documents with Vietnamese cultural intelligence...'
            }
          </span>
        </div>
      )}
    </div>
  );
};

// Business Context Analyzer Component
const VeriBusinessContextAnalyzer: React.FC<{
  veriBusinessContext: VeriBusinessProfile | null;
  veriLanguage: 'vietnamese' | 'english';
}> = ({ veriBusinessContext, veriLanguage }) => {
  const [veriAIAnalysis, setVeriAIAnalysis] = useState<VeriAIDocumentAnalysis | null>(null);
  const [veriAnalyzing, setVeriAnalyzing] = useState(false);

  useEffect(() => {
    if (veriBusinessContext) {
      analyzeBusinessContext();
    }
  }, [veriBusinessContext]);

  const analyzeBusinessContext = async () => {
    if (!veriBusinessContext) return;

    setVeriAnalyzing(true);
    try {
      const analysis = await veriDocumentAIService.analyzeBusinessForDocumentGeneration(
        veriBusinessContext,
        'privacy-policy'
      );
      setVeriAIAnalysis(analysis);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setVeriAnalyzing(false);
    }
  };

  if (!veriBusinessContext) {
    return (
      <div className="veri-business-context-placeholder">
        <p>
          {veriLanguage === 'vietnamese' ? 
            'Vui lòng cung cấp thông tin doanh nghiệp để AI phân tích' :
            'Please provide business information for AI analysis'
          }
        </p>
      </div>
    );
  }

  return (
    <div className="veri-business-context-analyzer">
      <div className="veri-analyzer-header">
        <h3 className="veri-analyzer-title">
          {veriLanguage === 'vietnamese' ? 'Phân tích AI Doanh nghiệp' : 'AI Business Analysis'}
        </h3>
        
        {veriAnalyzing && (
          <div className="veri-analyzing-indicator">
            <div className="veri-analyzing-spinner"></div>
            <span>
              {veriLanguage === 'vietnamese' ? 'Đang phân tích...' : 'Analyzing...'}
            </span>
          </div>
        )}
      </div>

      <div className="veri-business-summary">
        <div className="veri-business-info">
          <h4 className="veri-business-name">{veriBusinessContext.veriCompanyName}</h4>
          <div className="veri-business-details">
            <span className="veri-business-detail">
              {veriLanguage === 'vietnamese' ? 'Ngành:' : 'Industry:'} {veriBusinessContext.veriIndustryType}
            </span>
            <span className="veri-business-detail">
              {veriLanguage === 'vietnamese' ? 'Quy mô:' : 'Size:'} {veriBusinessContext.veriBusinessSize}
            </span>
            <span className="veri-business-detail">
              {veriLanguage === 'vietnamese' ? 'Khu vực:' : 'Region:'} {veriBusinessContext.veriRegionalLocation}
            </span>
          </div>
        </div>
      </div>

      {veriAIAnalysis && (
        <div className="veri-ai-analysis-results">
          <div className="veri-analysis-metrics">
            <div className="veri-analysis-metric">
              <label>{veriLanguage === 'vietnamese' ? 'Độ phức tạp:' : 'Complexity:'}</label>
              <span className={`veri-complexity-badge veri-${veriAIAnalysis.veriComplexityLevel}`}>
                {veriAIAnalysis.veriComplexityLevel.toUpperCase()}
              </span>
            </div>
            
            <div className="veri-analysis-metric">
              <label>{veriLanguage === 'vietnamese' ? 'Cá nhân hóa:' : 'Personalization:'}</label>
              <span className="veri-score">{Math.round(veriAIAnalysis.veriPersonalizationScore * 100)}%</span>
            </div>
            
            <div className="veri-analysis-metric">
              <label>{veriLanguage === 'vietnamese' ? 'Độ tin cậy AI:' : 'AI Confidence:'}</label>
              <span className="veri-score">{Math.round(veriAIAnalysis.veriAIConfidence * 100)}%</span>
            </div>
          </div>

          <div className="veri-cultural-analysis">
            <h5>{veriLanguage === 'vietnamese' ? 'Phong cách Văn hóa:' : 'Cultural Style:'}</h5>
            <p className="veri-cultural-style">{veriAIAnalysis.veriCulturalStyle}</p>
          </div>

          <div className="veri-industry-requirements">
            <h5>{veriLanguage === 'vietnamese' ? 'Yêu cầu theo Ngành:' : 'Industry Requirements:'}</h5>
            <p className="veri-industry-desc">{veriAIAnalysis.veriIndustrySpecificRequirements}</p>
          </div>
        </div>
      )}
    </div>
  );
};

// Document Generator Actions Component
const VeriDocumentGeneratorActions: React.FC<{
  veriSelectedDocuments: VeriDocumentType[];
  veriBusinessContext: VeriBusinessProfile | null;
  veriLanguage: 'vietnamese' | 'english';
  veriOnGenerate: (documents: VeriGeneratedDocument[]) => void;
}> = ({ veriSelectedDocuments, veriBusinessContext, veriLanguage, veriOnGenerate }) => {
  const [veriGenerating, setVeriGenerating] = useState(false);

  const handleGenerateDocuments = async () => {
    if (!veriBusinessContext || veriSelectedDocuments.length === 0) return;

    setVeriGenerating(true);
    try {
      const generatedDocs: VeriGeneratedDocument[] = [];
      
      for (const docType of veriSelectedDocuments) {
        const doc = await veriDocumentAIService.generateDocument(
          docType,
          veriBusinessContext,
          veriLanguage
        );
        generatedDocs.push(doc);
      }
      
      veriOnGenerate(generatedDocs);
    } catch (error) {
      console.error('Document generation failed:', error);
    } finally {
      setVeriGenerating(false);
    }
  };

  const isGenerateDisabled = !veriBusinessContext || veriSelectedDocuments.length === 0 || veriGenerating;

  return (
    <div className="veri-generator-actions">
      <button
        className="veri-generate-button"
        onClick={handleGenerateDocuments}
        disabled={isGenerateDisabled}
      >
        {veriGenerating ? (
          <>
            <div className="veri-button-spinner"></div>
            {veriLanguage === 'vietnamese' ? 'Đang tạo tài liệu...' : 'Generating documents...'}
          </>
        ) : (
          <>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2L3 7v11h4v-6h6v6h4V7l-7-5z"/>
            </svg>
            {veriLanguage === 'vietnamese' ? 
              `Tạo ${veriSelectedDocuments.length} Tài liệu` :
              `Generate ${veriSelectedDocuments.length} Documents`
            }
          </>
        )}
      </button>

      {isGenerateDisabled && (
        <p className="veri-generate-help">
          {veriLanguage === 'vietnamese' ? 
            'Vui lòng chọn tài liệu và cung cấp thông tin doanh nghiệp' :
            'Please select documents and provide business information'
          }
        </p>
      )}
    </div>
  );
};

// Main Vietnamese Document Generation System Component
export const VeriDocumentGenerationSystem: React.FC<VeriDocumentGenerationProps> = ({
  veriBusinessContext: initialBusinessContext,
  veriLanguage: initialLanguage = 'vietnamese',
  veriOnComplete,
  veriOnStepChange,
  veriCulturalStyle,
  veriSelectedDocuments: initialSelectedDocuments = []
}) => {
  // Set page title
  usePageTitle({ 
    title: 'Document Generation', 
    titleVi: 'Tạo Tài liệu' 
  });
  
  // Log step changes for future implementation
  const logStepChange = (step: string) => {
    if (veriOnStepChange) {
      veriOnStepChange(step);
    }
  };

  const [veriSelectedDocuments, setVeriSelectedDocuments] = useState<VeriDocumentType[]>(initialSelectedDocuments);
  const [veriLanguage, setVeriLanguage] = useState<'vietnamese' | 'english'>(initialLanguage);
  const [veriBusinessContext, setVeriBusinessContext] = useState<VeriBusinessProfile | null>(initialBusinessContext || null);
  const [veriAIGenerator, setVeriAIGenerator] = useState<VeriAIDocumentGenerator | null>(null);
  const [veriGenerationStatus, setVeriGenerationStatus] = useState<VeriDocumentGenerationStatus | null>(null);
  const [veriGeneratedDocuments, setVeriGeneratedDocuments] = useState<VeriGeneratedDocument[]>([]);

  // Initialize generation status when documents are selected
  useEffect(() => {
    if (veriSelectedDocuments.length > 0 && !veriGenerationStatus) {
      const initialStatus: VeriDocumentGenerationStatus = {
        veriStatus: 'pending',
        veriProgress: 0,
        veriCurrentStep: 'document-selection',
        veriEstimatedTimeRemaining: 0,
        veriGeneratedSections: [],
        veriValidationResults: []
      };
      setVeriGenerationStatus(initialStatus);
      logStepChange('documents-selected');
    }
  }, [veriSelectedDocuments, veriGenerationStatus]);

  // Initialize default business context if not provided
  useEffect(() => {
    if (!veriBusinessContext) {
      const defaultContext: VeriBusinessProfile = {
        veriCompanyName: 'Công ty TNHH ABC',
        veriIndustryType: 'technology',
        veriBusinessSize: 'sme',
        veriEmployeeCount: 50,
        veriRegionalLocation: 'south',
        veriDataProcessingVolume: 'medium',
        veriCommunicationStyle: 'modern',
        veriStakeholderTypes: ['customers', 'employees', 'partners']
      };
      setVeriBusinessContext(defaultContext);
    }
  }, [veriBusinessContext]);

  // Initialize AI Generator
  useEffect(() => {
    if (!veriAIGenerator) {
      const defaultAIGenerator: VeriAIDocumentGenerator = {
        veriEngineId: 'veri_document_ai_v3',
        veriEngineVersion: '3.0.0',
        veriCapabilities: ['document_generation', 'cultural_adaptation', 'legal_validation'],
        veriLanguages: ['vietnamese', 'english'],
        veriDocumentTypes: [
          'privacy-policy', 'privacy-notice', 'consent-forms', 'data-processing-agreement',
          'data-subject-rights-procedure', 'security-incident-response-plan', 'data-retention-policy',
          'cross-border-transfer-agreement', 'dpo-appointment-letter', 'compliance-audit-checklist'
        ],
        veriCulturalModels: ['north_vietnam', 'central_vietnam', 'south_vietnam'],
        veriAnalysisTypes: ['business_context', 'legal_requirements', 'cultural_adaptation']
      };
      setVeriAIGenerator(defaultAIGenerator);
    }
  }, [veriAIGenerator]);

  const getVeriAvailableDocuments = (): VeriDocumentType[] => {
    return [
      'privacy-policy',
      'privacy-notice', 
      'consent-forms',
      'data-processing-agreement',
      'data-subject-rights-procedure',
      'security-incident-response-plan',
      'data-retention-policy',
      'cross-border-transfer-agreement',
      'dpo-appointment-letter',
      'compliance-audit-checklist',
      'employee-privacy-training-materials',
      'vendor-privacy-assessment'
    ];
  };

  const handleVeriLanguageChange = (language: 'vietnamese' | 'english') => {
    setVeriLanguage(language);
  };

  const handleVeriDocumentGeneration = async (documents: VeriGeneratedDocument[]) => {
    setVeriGeneratedDocuments(documents);
    if (veriOnComplete) {
      documents.forEach(doc => veriOnComplete(doc));
    }
  };

  return (
    <VeriDocumentGenerationProvider
      veriLanguage={veriLanguage}
      veriBusinessContext={veriBusinessContext}
      veriAIGenerator={veriAIGenerator}
    >
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-green-50" style={{
        background: 'linear-gradient(135deg, #f0f4f0 0%, #f1f6fb 25%, #f0f4f0 50%, #f1f6fb 75%, #f0f4f0 100%)'
      }}>
        <VeriSyntraBanner
          variant="portal"
          customTitle="VeriPortal"
          customSubtitle={veriLanguage === 'vietnamese' ? 'Hệ thống Tạo Tài liệu Pháp lý AI' : 'AI Legal Document Generation System'}
          currentLanguage={veriLanguage === 'vietnamese' ? 'vi' : 'en'}
          onLanguageChange={(lang) => handleVeriLanguageChange(lang === 'vi' ? 'vietnamese' : 'english')}
          showConnectionStatus={true}
          showLanguageToggle={true}
        />

        <div className="veri-document-layout" style={{
          background: veriCulturalStyle === 'north' ? 'rgba(247, 250, 247, 0.9)' :
                     veriCulturalStyle === 'central' ? 'rgba(248, 251, 253, 0.9)' :
                     'rgba(248, 250, 252, 0.9)'
        }}>
          <div className="veri-document-header">
            <div className="veri-document-header-content">
              <h1 className="veri-document-title">
                {veriLanguage === 'vietnamese' ? 
                  'Hệ thống Tạo Tài liệu Pháp lý Việt Nam' : 
                  'Vietnamese Legal Document Generation System'}
              </h1>
              <p className="veri-document-subtitle">
                {veriLanguage === 'vietnamese' ? 
                  'AI tạo tài liệu tuân thủ PDPL 2025 với trí tuệ văn hóa Việt Nam' :
                  'AI generates PDPL 2025 compliant documents with Vietnamese cultural intelligence'}
              </p>
            </div>
            
            <div className="veri-portal-navigation">
              <a 
                href="/veriportal" 
                className="veri-nav-link"
                style={{
                  background: 'linear-gradient(135deg, var(--veri-sage-green), var(--veri-ocean-blue))',
                  color: 'white',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontWeight: '500',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 6px 20px rgba(107, 142, 107, 0.4)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 2L3 7v11h4v-6h6v6h4V7l-7-5z"/>
                  <path d="M10 8L4 12v6h2v-4h8v4h2v-6l-6-4z"/>
                </svg>
                {veriLanguage === 'vietnamese' ? 'Quay về Wizards' : 'Back to Wizards'}
              </a>
            </div>
          </div>

          <div className="veri-document-main-content">
            <div className="veri-document-sidebar">
              <VeriBusinessContextAnalyzer
                veriBusinessContext={veriBusinessContext}
                veriLanguage={veriLanguage}
              />
              
              <VeriDocumentGenerationProgress
                veriSelectedDocuments={veriSelectedDocuments}
                veriGenerationStatus={veriGenerationStatus || undefined}
                veriLanguage={veriLanguage}
              />
            </div>

            <div className="veri-document-content">
              <VeriDocumentTypeSelector
                veriAvailableDocuments={getVeriAvailableDocuments()}
                veriSelectedDocuments={veriSelectedDocuments}
                veriOnDocumentSelection={setVeriSelectedDocuments}
                veriLanguage={veriLanguage}
              />

              <VeriDocumentGeneratorActions
                veriSelectedDocuments={veriSelectedDocuments}
                veriBusinessContext={veriBusinessContext}
                veriLanguage={veriLanguage}
                veriOnGenerate={handleVeriDocumentGeneration}
              />

              {veriGeneratedDocuments.length > 0 && (
                <div className="veri-generated-documents">
                  <h3>
                    {veriLanguage === 'vietnamese' ? 'Tài liệu đã Tạo' : 'Generated Documents'}
                  </h3>
                  {veriGeneratedDocuments.map(doc => (
                    <div key={doc.veriDocumentId} className="veri-generated-document-card">
                      <h4>{doc.veriDocumentContent.veriDocumentMetadata.veriTitle}</h4>
                      <p>
                        {veriLanguage === 'vietnamese' ? 'Độ tin cậy AI:' : 'AI Confidence:'} 
                        {Math.round(doc.veriAIPersonalizationScore * 100)}%
                      </p>
                      <button className="veri-download-button">
                        {veriLanguage === 'vietnamese' ? 'Tải xuống' : 'Download'}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </VeriDocumentGenerationProvider>
  );
};

export default VeriDocumentGenerationSystem;