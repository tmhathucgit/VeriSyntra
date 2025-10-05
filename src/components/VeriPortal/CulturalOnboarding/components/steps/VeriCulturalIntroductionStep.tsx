// VeriPortal Cultural Introduction Step - Vietnamese Cultura          <p className=\"mt-2 text-gray-600 veri-loading-text-small\">Đang tải bản dịch...</p> Component
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
  const { t, i18n, ready } = useTranslation(['common', 'veriportal']);

  console.log(`🏁 VeriCulturalIntroductionStep: Rendering with language ${veriLanguage} at ${new Date().toLocaleTimeString()}`);
  console.log(`🔍 Debug - i18n.language: ${i18n.language}, veriLanguage: ${veriLanguage}, i18n ready: ${ready}`);
  console.log(`🔍 Debug - Translation test: ${t('veriportal:culturalIntroduction.title')}`);
  
  // Update i18n language when veriLanguage prop changes
  useEffect(() => {
    const newLang = veriLanguage === 'vietnamese' ? 'vi' : 'en';
    console.log(`📝 VeriCulturalIntroductionStep: Language changing to ${veriLanguage} (i18n: ${newLang})`);
    console.log(`📝 Before change - i18n.language: ${i18n.language}`);
    
    if (i18n.language !== newLang) {
      i18n.changeLanguage(newLang).then(() => {
        console.log(`🌐 i18n language changed to ${newLang}`);
        console.log(`🔍 After change - Translation test: ${t('veriportal:culturalIntroduction.title')}`);
      });
    }
  }, [veriLanguage, i18n, t]);

  const veriProceedToNextStep = () => {
    veriOnNext('business-profile-setup');
  };

  // Show loading state if i18n is not ready
  if (!ready) {
    return (
      <div className="space-y-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading translations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome section has been moved to the main layout above the progress card */}
      
      {/* Features Grid - Landing Page Style */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-2xl">
              🇻🇳
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">
                {veriLanguage === 'vietnamese' ? 'Giao diện Việt hóa' : 'Vietnamese Interface'}
              </h3>
              <p className="text-sm text-gray-600">
                {veriLanguage === 'vietnamese' 
                  ? 'Giao diện tiếng Việt tối ưu với văn hóa địa phương'
                  : 'Vietnamese-optimized interface with local cultural adaptation'
                }
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center text-2xl">
              🏢
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">
                {veriLanguage === 'vietnamese' ? 'Hiểu biết kinh doanh' : 'Business Understanding'}
              </h3>
              <p className="text-sm text-gray-600">
                {veriLanguage === 'vietnamese'
                  ? 'Hiểu biết sâu về phân cấp và quy trình kinh doanh Việt Nam'
                  : 'Deep understanding of Vietnamese business hierarchy and processes'
                }
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center text-2xl">
              ⚖️
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">
                {veriLanguage === 'vietnamese' ? 'Tuân thủ PDPL' : 'PDPL Compliance'}
              </h3>
              <p className="text-sm text-gray-600">
                {veriLanguage === 'vietnamese'
                  ? 'Tuân thủ PDPL 2025 với bối cảnh kinh doanh Việt Nam'
                  : 'PDPL 2025 compliance with Vietnamese business context'
                }
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Cultural Detection Section - Landing Page Style */}
      {veriCulturalContext && (
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            {veriLanguage === 'vietnamese' 
              ? '🤖 AI đã phát hiện văn hóa của bạn' 
              : '🤖 AI Detected Your Culture'
            }
          </h3>
          <div className="flex flex-wrap gap-4">
            <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-orange-100 to-emerald-100 px-4 py-2 rounded-full">
              <span className="text-lg">
                {veriCulturalContext.veriRegion === 'north' && '🏔️'}
                {veriCulturalContext.veriRegion === 'central' && '🏖️'}
                {veriCulturalContext.veriRegion === 'south' && '🏙️'}
              </span>
              <span className="font-medium text-gray-800">
                {veriCulturalContext.veriRegion === 'north' && (veriLanguage === 'vietnamese' ? 'Miền Bắc' : 'Northern Vietnam')}
                {veriCulturalContext.veriRegion === 'central' && (veriLanguage === 'vietnamese' ? 'Miền Trung' : 'Central Vietnam')}
                {veriCulturalContext.veriRegion === 'south' && (veriLanguage === 'vietnamese' ? 'Miền Nam' : 'Southern Vietnam')}
              </span>
            </div>
            <div className="inline-flex items-center space-x-2 bg-teal-100 px-4 py-2 rounded-full">
              <span className="font-medium text-teal-800">
                {veriLanguage === 'vietnamese' 
                  ? `${veriCulturalContext.veriCommunicationStyle === 'formal' ? 'Trang trọng' : 
                      veriCulturalContext.veriCommunicationStyle === 'balanced' ? 'Cân bằng' : 'Thân thiện'}`
                  : veriCulturalContext.veriCommunicationStyle
                }
              </span>
            </div>
          </div>
        </div>
      )}
      
      {/* Action Button - Vietnamese Cultural Style */}
      <div className="text-center">
        <button 
          onClick={veriProceedToNextStep}
          className="group text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 flex items-center justify-center space-x-2 mx-auto"
          style={{
            background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #d4c18a 100%)',
            border: '2px solid #d4c18a',
            boxShadow: '0 4px 20px rgba(107, 142, 107, 0.25)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = '0 6px 32px rgba(107, 142, 107, 0.35)';
            e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #8bb3d3 50%, #dcc898 100%)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = '0 4px 20px rgba(107, 142, 107, 0.25)';
            e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #d4c18a 100%)';
          }}
        >
          <span>{t('veriportal:culturalIntroduction.nextAction')}</span>
          <span className="text-lg group-hover:translate-x-1 transition-transform">➡️</span>
        </button>
        
        {/* Statistics Section - Landing Page Style */}
        <div className="flex justify-center items-center space-x-8 pt-8 text-sm text-gray-600">
          <div>
            <div className="text-2xl font-bold text-gray-900">🇻🇳</div>
            <div>{veriLanguage === 'vietnamese' ? 'Văn hóa Việt' : 'Vietnamese Culture'}</div>
          </div>
          <div className="h-8 w-px bg-gray-300"></div>
          <div>
            <div className="text-2xl font-bold text-gray-900">⚖️</div>
            <div>PDPL 2025</div>
          </div>
          <div className="h-8 w-px bg-gray-300"></div>
          <div>
            <div className="text-2xl font-bold text-gray-900">🏢</div>
            <div>{veriLanguage === 'vietnamese' ? 'Doanh nghiệp' : 'Business'}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VeriCulturalIntroductionStep;