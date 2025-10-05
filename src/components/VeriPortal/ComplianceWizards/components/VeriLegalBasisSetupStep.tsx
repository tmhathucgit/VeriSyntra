// VeriLegalBasisSetupStep Component
// AI-Powered Vietnamese Legal Basis Setup for PDPL 2025

import React, { useState, useEffect } from 'react';
import {
  VeriLegalBasisProps,
  VeriLegalBasisData,
  VeriLegalBasisRecommendation,
  VeriValidationResult,
  VeriAIComplianceAnalysis
} from '../types';
import { veriComplianceAIService } from '../services/veriComplianceAIServices';

export const VeriLegalBasisSetupStep: React.FC<VeriLegalBasisProps> = ({
  veriBusinessContext,
  veriLanguage,
  veriAIAnalysis,
  veriOnComplete
}) => {
  const [veriLegalBasisData, setVeriLegalBasisData] = useState<VeriLegalBasisData>({
    veriSelectedBases: [],
    veriProcessingPurposes: {},
    veriDataCategories: {},
    veriRetentionPeriods: {},
    veriLegalDocuments: []
  });
  const [veriAIRecommendations, setVeriAIRecommendations] = useState<VeriLegalBasisRecommendation[]>([]);
  const [veriValidationResult, setVeriValidationResult] = useState<VeriValidationResult | null>(null);
  const [veriIsLoading, setVeriIsLoading] = useState(false);
  const [veriShowRecommendations, setVeriShowRecommendations] = useState(true);

  const veriLegalBasisContent = {
    vietnamese: {
      veriTitle: "Xác định Cơ sở Pháp lý cho Xử lý Dữ liệu",
      veriDescription: "AI đã phân tích doanh nghiệp của bạn và đề xuất cơ sở pháp lý phù hợp",
      veriLegalBases: {
        consent: {
          veriName: "Đồng ý của Chủ thể Dữ liệu",
          veriDescription: "Phù hợp cho: Marketing, Newsletter, Dịch vụ không bắt buộc",
          veriVietnameseContext: "Thường dùng cho doanh nghiệp B2C và marketing"
        },
        contract: {
          veriName: "Thực hiện Hợp đồng",
          veriDescription: "Phù hợp cho: Giao dịch, Thanh toán, Giao hàng",
          veriVietnameseContext: "Cơ sở chính cho thương mại điện tử Việt Nam"
        },
        legal_obligation: {
          veriName: "Nghĩa vụ Pháp lý",
          veriDescription: "Phù hợp cho: Thuế, Kế toán, Báo cáo Chính phủ",
          veriVietnameseContext: "Bắt buộc cho báo cáo thuế và Bộ Công an"
        },
        legitimate_interest: {
          veriName: "Lợi ích Chính đáng",
          veriDescription: "Phù hợp cho: Bảo mật, Phòng chống gian lận",
          veriVietnameseContext: "Cần cân nhắc cẩn thận theo luật Việt Nam"
        }
      }
    },
    english: {
      veriTitle: "Determine Legal Basis for Data Processing",
      veriDescription: "AI has analyzed your business and recommended appropriate legal bases",
      veriLegalBases: {
        consent: {
          veriName: "Data Subject Consent",
          veriDescription: "Suitable for: Marketing, Newsletters, Non-essential services",
          veriVietnameseContext: "Commonly used for B2C businesses and marketing"
        },
        contract: {
          veriName: "Contract Performance",
          veriDescription: "Suitable for: Transactions, Payments, Delivery",
          veriVietnameseContext: "Primary basis for Vietnamese e-commerce"
        },
        legal_obligation: {
          veriName: "Legal Obligation",
          veriDescription: "Suitable for: Tax, Accounting, Government reporting",
          veriVietnameseContext: "Required for tax reporting and MPS compliance"
        },
        legitimate_interest: {
          veriName: "Legitimate Interest",
          veriDescription: "Suitable for: Security, Fraud prevention",
          veriVietnameseContext: "Requires careful consideration under Vietnamese law"
        }
      }
    }
  };

  // Load AI recommendations on component mount
  useEffect(() => {
    const loadRecommendations = async () => {
      setVeriIsLoading(true);
      try {
        const recommendations = await veriComplianceAIService.analyzeVeriBusinessForLegalBasis(veriBusinessContext);
        setVeriAIRecommendations(recommendations);
      } catch (error) {
        console.error('Failed to load AI recommendations:', error);
      } finally {
        setVeriIsLoading(false);
      }
    };

    loadRecommendations();
  }, [veriBusinessContext]);

  // Validate on data changes
  useEffect(() => {
    const validateData = async () => {
      if (veriLegalBasisData.veriSelectedBases.length > 0) {
        try {
          const validation = await veriComplianceAIService.validateVeriLegalBasisCompliance(
            veriLegalBasisData, 
            veriBusinessContext
          );
          setVeriValidationResult(validation);
        } catch (error) {
          console.error('Validation error:', error);
        }
      }
    };

    validateData();
  }, [veriLegalBasisData, veriBusinessContext]);

  // Complete step when validation passes
  useEffect(() => {
    if (veriValidationResult?.veriIsValid) {
      veriOnComplete(veriLegalBasisData);
    }
  }, [veriValidationResult, veriLegalBasisData, veriOnComplete]);

  const veriHandleLegalBasisSelection = (basisKey: string, checked: boolean) => {
    setVeriLegalBasisData(prev => {
      const updatedBases = checked
        ? [...prev.veriSelectedBases, basisKey]
        : prev.veriSelectedBases.filter(basis => basis !== basisKey);
      
      return {
        ...prev,
        veriSelectedBases: updatedBases
      };
    });
  };

  const updateVeriProcessingPurposes = (basisKey: string, purposes: string[]) => {
    setVeriLegalBasisData(prev => ({
      ...prev,
      veriProcessingPurposes: {
        ...prev.veriProcessingPurposes,
        [basisKey]: purposes
      }
    }));
  };

  const veriAcceptLegalBasisRecommendation = (recommendation: VeriLegalBasisRecommendation) => {
    const basisKey = recommendation.veriLegalBasisName;
    veriHandleLegalBasisSelection(basisKey, true);
    
    // Auto-fill some processing purposes based on the recommendation
    const defaultPurposes = getDefaultProcessingPurposes(basisKey);
    updateVeriProcessingPurposes(basisKey, defaultPurposes);
  };

  const veriCustomizeLegalBasisRecommendation = (recommendation: VeriLegalBasisRecommendation) => {
    // For now, just accept the recommendation (customization UI can be added later)
    veriAcceptLegalBasisRecommendation(recommendation);
  };

  const getDefaultProcessingPurposes = (basisKey: string): string[] => {
    const purposeMap: Record<string, string[]> = {
      consent: ['Marketing communications', 'Newsletter subscriptions', 'Product recommendations'],
      contract: ['Order processing', 'Payment processing', 'Delivery management', 'Customer support'],
      legal_obligation: ['Tax reporting', 'Government compliance', 'Legal record keeping'],
      legitimate_interest: ['Fraud prevention', 'Security monitoring', 'System administration']
    };
    
    return purposeMap[basisKey] || [];
  };

  const isVeriAIRecommended = (basisKey: string): boolean => {
    return veriAIRecommendations.some(rec => rec.veriLegalBasisName === basisKey);
  };

  const getRecommendationPriority = (basisKey: string): 'low' | 'medium' | 'high' | 'critical' | null => {
    const recommendation = veriAIRecommendations.find(rec => rec.veriLegalBasisName === basisKey);
    return recommendation?.veriPriorityLevel || null;
  };

  const getRecommendationMatch = (basisKey: string): number => {
    const recommendation = veriAIRecommendations.find(rec => rec.veriLegalBasisName === basisKey);
    return recommendation?.veriBusinessMatch || 0;
  };

  if (veriIsLoading) {
    return (
      <div className="veri-legal-basis-loading">
        <div className="veri-ai-analysis-spinner">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
            <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2" fill="none">
              <animate attributeName="stroke-dasharray" dur="2s" values="0 87.96;43.98 43.98;0 87.96" repeatCount="indefinite"/>
              <animate attributeName="stroke-dashoffset" dur="2s" values="0;-21.99;-87.96" repeatCount="indefinite"/>
            </circle>
          </svg>
        </div>
        <p>
          {veriLanguage === 'vietnamese' 
            ? 'AI đang phân tích và tạo đề xuất cơ sở pháp lý...'
            : 'AI is analyzing and generating legal basis recommendations...'}
        </p>
      </div>
    );
  }

  return (
    <div className="veri-legal-basis-step-container">
      <div className="veri-step-header">
        <h3 className="veri-step-title">{veriLegalBasisContent[veriLanguage].veriTitle}</h3>
        <div className="veri-ai-analysis-indicator">
          <div className="veri-ai-brain veri-active">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
              <path d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"/>
            </svg>
          </div>
          <span className="veri-ai-analysis-text">
            {veriLegalBasisContent[veriLanguage].veriDescription}
          </span>
        </div>
      </div>

      {veriShowRecommendations && veriAIRecommendations.length > 0 && (
        <div className="veri-ai-recommendations">
          <div className="veri-recommendation-header">
            <h4>
              {veriLanguage === 'vietnamese' 
                ? 'Đề xuất từ AI dựa trên phân tích doanh nghiệp' 
                : 'AI Recommendations based on business analysis'}
            </h4>
            <button 
              className="veri-toggle-recommendations"
              onClick={() => setVeriShowRecommendations(false)}
            >
              {veriLanguage === 'vietnamese' ? 'Ẩn' : 'Hide'}
            </button>
          </div>
          
          {veriAIRecommendations.map((recommendation, index) => (
            <div key={index} className="veri-ai-recommendation-card">
              <div className={`veri-recommendation-priority veri-${recommendation.veriPriorityLevel}`}>
                {recommendation.veriPriorityLevel === 'high' ? 
                  (veriLanguage === 'vietnamese' ? 'Ưu tiên cao' : 'High Priority') :
                  (veriLanguage === 'vietnamese' ? 'Khuyến nghị' : 'Recommended')
                }
              </div>
              
              <div className="veri-recommendation-content">
                <h5 className="veri-recommendation-title">
                  {veriLegalBasisContent[veriLanguage].veriLegalBases[recommendation.veriLegalBasisName as keyof typeof veriLegalBasisContent['vietnamese']['veriLegalBases']]?.veriName || recommendation.veriLegalBasisName}
                </h5>
                <p className="veri-recommendation-reason">{recommendation.veriVietnameseReason}</p>
                <div className="veri-business-context-match">
                  <div className={`veri-match-indicator veri-score-${Math.round(recommendation.veriBusinessMatch / 10) * 10}`}>
                    <div 
                      className="veri-match-fill"
                      style={{ width: `${recommendation.veriBusinessMatch}%` }}
                    />
                  </div>
                  <span className="veri-match-text">
                    {veriLanguage === 'vietnamese' ? 
                      `Phù hợp ${recommendation.veriBusinessMatch}% với doanh nghiệp của bạn` :
                      `${recommendation.veriBusinessMatch}% match with your business`
                    }
                  </span>
                </div>
              </div>
              
              <div className="veri-recommendation-actions">
                <button
                  className="veri-accept-recommendation-button"
                  onClick={() => veriAcceptLegalBasisRecommendation(recommendation)}
                >
                  {veriLanguage === 'vietnamese' ? 'Chấp nhận' : 'Accept'}
                </button>
                
                <button
                  className="veri-customize-recommendation-button"
                  onClick={() => veriCustomizeLegalBasisRecommendation(recommendation)}
                >
                  {veriLanguage === 'vietnamese' ? 'Tùy chỉnh' : 'Customize'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="veri-legal-basis-selection">
        <div className="veri-selection-header">
          <h4>
            {veriLanguage === 'vietnamese' 
              ? 'Chọn Cơ sở Pháp lý cho Hoạt động Xử lý Dữ liệu' 
              : 'Select Legal Basis for Data Processing Activities'}
          </h4>
          {!veriShowRecommendations && veriAIRecommendations.length > 0 && (
            <button 
              className="veri-show-recommendations"
              onClick={() => setVeriShowRecommendations(true)}
            >
              {veriLanguage === 'vietnamese' ? 'Hiện đề xuất AI' : 'Show AI Recommendations'}
            </button>
          )}
        </div>
        
        {Object.entries(veriLegalBasisContent[veriLanguage].veriLegalBases).map(([basisKey, basisInfo]) => (
          <div key={basisKey} className="veri-legal-basis-option">
            <div 
              className={`veri-legal-basis-card ${
                veriLegalBasisData.veriSelectedBases.includes(basisKey) ? 'veri-selected' : ''
              } ${
                isVeriAIRecommended(basisKey) ? 'veri-ai-recommended' : ''
              }`}
            >
              <div className="veri-legal-basis-header">
                <label className="veri-legal-basis-checkbox-label">
                  <input
                    type="checkbox"
                    className="veri-legal-basis-checkbox"
                    checked={veriLegalBasisData.veriSelectedBases.includes(basisKey)}
                    onChange={(e) => veriHandleLegalBasisSelection(basisKey, e.target.checked)}
                  />
                  <span className="veri-legal-basis-name">{basisInfo.veriName}</span>
                </label>
                {isVeriAIRecommended(basisKey) && (
                  <div className={`veri-ai-recommended-badge veri-${getRecommendationPriority(basisKey)}`}>
                    <span>AI {getRecommendationMatch(basisKey)}%</span>
                  </div>
                )}
              </div>
              
              <p className="veri-legal-basis-description">{basisInfo.veriDescription}</p>
              <p className="veri-vietnamese-context">{basisInfo.veriVietnameseContext}</p>
              
              {veriLegalBasisData.veriSelectedBases.includes(basisKey) && (
                <div className="veri-legal-basis-details">
                  <div className="veri-processing-purposes">
                    <h5>
                      {veriLanguage === 'vietnamese' ? 'Mục đích Xử lý:' : 'Processing Purposes:'}
                    </h5>
                    <div className="veri-purposes-list">
                      {getDefaultProcessingPurposes(basisKey).map((purpose, index) => (
                        <div key={index} className="veri-purpose-item">
                          <label className="veri-purpose-checkbox-label">
                            <input
                              type="checkbox"
                              checked={veriLegalBasisData.veriProcessingPurposes[basisKey]?.includes(purpose) || false}
                              onChange={(e) => {
                                const currentPurposes = veriLegalBasisData.veriProcessingPurposes[basisKey] || [];
                                const updatedPurposes = e.target.checked
                                  ? [...currentPurposes, purpose]
                                  : currentPurposes.filter(p => p !== purpose);
                                updateVeriProcessingPurposes(basisKey, updatedPurposes);
                              }}
                            />
                            <span>{purpose}</span>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {veriValidationResult && (
        <div className="veri-validation-results">
          {veriValidationResult.veriErrors.length > 0 && (
            <div className="veri-validation-errors">
              <h5>{veriLanguage === 'vietnamese' ? 'Lỗi cần sửa:' : 'Errors to fix:'}</h5>
              {veriValidationResult.veriErrors.map((error, index) => (
                <div key={index} className="veri-validation-error">
                  <span className="veri-error-message">
                    {veriLanguage === 'vietnamese' ? error.veriMessageVi : error.veriMessage}
                  </span>
                </div>
              ))}
            </div>
          )}
          
          {veriValidationResult.veriWarnings.length > 0 && (
            <div className="veri-validation-warnings">
              <h5>{veriLanguage === 'vietnamese' ? 'Cảnh báo:' : 'Warnings:'}</h5>
              {veriValidationResult.veriWarnings.map((warning, index) => (
                <div key={index} className="veri-validation-warning">
                  <span className="veri-warning-message">
                    {veriLanguage === 'vietnamese' ? warning.veriMessageVi : warning.veriMessage}
                  </span>
                </div>
              ))}
            </div>
          )}
          
          {veriValidationResult.veriSuggestions.length > 0 && (
            <div className="veri-validation-suggestions">
              <h5>{veriLanguage === 'vietnamese' ? 'Gợi ý cải thiện:' : 'Improvement suggestions:'}</h5>
              {veriValidationResult.veriSuggestions.map((suggestion, index) => (
                <div key={index} className="veri-validation-suggestion">
                  <span className="veri-suggestion-message">
                    {veriLanguage === 'vietnamese' ? suggestion.veriMessageVi : suggestion.veriMessage}
                  </span>
                </div>
              ))}
            </div>
          )}
          
          {veriValidationResult.veriIsValid && (
            <div className="veri-validation-success">
              <div className="veri-success-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                </svg>
              </div>
              <span>
                {veriLanguage === 'vietnamese' 
                  ? 'Cơ sở pháp lý đã được thiết lập hợp lệ!' 
                  : 'Legal basis has been set up successfully!'}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};