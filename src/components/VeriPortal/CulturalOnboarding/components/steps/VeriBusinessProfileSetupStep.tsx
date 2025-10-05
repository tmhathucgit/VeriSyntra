// VeriPortal Business Profile Setup Step - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React, { useState } from 'react';
import {
  VeriOnboardingStep,
  VeriCulturalContext,
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine,
  VeriAIInsights,
  VeriBusinessProfile
} from '../../types';
import './VeriBusinessProfileSetupStep.css';

interface VeriBusinessProfileSetupStepProps {
  veriLanguage: 'vietnamese' | 'english';
  veriCulturalContext?: VeriCulturalContext;
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
  veriAIInsights?: VeriAIInsights[];
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriBusinessProfileSetupStep: React.FC<VeriBusinessProfileSetupStepProps> = ({
  veriLanguage,
  veriOnNext,
  veriOnPrevious
}) => {
  const [veriBusinessProfile, setVeriBusinessProfile] = useState<Partial<VeriBusinessProfile>>({
    veriBusinessName: '',
    veriBusinessType: 'sme',
    veriRegionalLocation: 'south',
    veriEmployeeCount: 0
  });

  const veriContent = {
    vietnamese: {
      title: 'Thông tin Doanh nghiệp',
      description: 'Vui lòng cung cấp thông tin để chúng tôi tùy chỉnh trải nghiệm phù hợp',
      businessName: 'Tên doanh nghiệp',
      businessType: 'Loại hình kinh doanh',
      region: 'Khu vực hoạt động',
      employees: 'Số lượng nhân viên',
      next: 'Tiếp tục',
      back: 'Quay lại'
    },
    english: {
      title: 'Business Information',
      description: 'Please provide information so we can customize your experience',
      businessName: 'Business Name',
      businessType: 'Business Type',
      region: 'Regional Location',
      employees: 'Number of Employees',
      next: 'Continue',
      back: 'Back'
    }
  };

  const veriBusinessTypes = {
    sme: { vi: 'Doanh nghiệp vừa và nhỏ', en: 'Small & Medium Enterprise' },
    startup: { vi: 'Công ty khởi nghiệp', en: 'Startup Company' },
    enterprise: { vi: 'Doanh nghiệp lớn', en: 'Large Enterprise' },
    government: { vi: 'Cơ quan Chính phủ', en: 'Government Agency' }
  };

  const veriRegions = {
    north: { vi: 'Miền Bắc', en: 'Northern Vietnam' },
    central: { vi: 'Miền Trung', en: 'Central Vietnam' },
    south: { vi: 'Miền Nam', en: 'Southern Vietnam' }
  };

  const veriHandleInputChange = (field: keyof VeriBusinessProfile, value: any) => {
    setVeriBusinessProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const veriProceedToNext = () => {
    veriOnNext('regional-adaptation');
  };

  const veriGoBack = () => {
    veriOnPrevious('cultural-introduction');
  };

  return (
    <div className="veri-business-profile-container">
      <div className="veri-step-header">
        <h2 className="veri-step-title">
          {veriContent[veriLanguage].title}
        </h2>
        <p className="veri-step-description">
          {veriContent[veriLanguage].description}
        </p>
      </div>

      <form className="veri-business-profile-form">
        <div className="veri-form-section">
          <div className="veri-input-group">
            <label className="veri-input-label">
              {veriContent[veriLanguage].businessName}
            </label>
            <input
              type="text"
              className="veri-input-field"
              value={veriBusinessProfile.veriBusinessName || ''}
              onChange={(e) => veriHandleInputChange('veriBusinessName', e.target.value)}
              placeholder={veriLanguage === 'vietnamese' ? 'Nhập tên công ty' : 'Enter company name'}
              required
            />
          </div>
          
          <div className="veri-input-group">
            <label className="veri-input-label">
              {veriContent[veriLanguage].businessType}
            </label>
            <select
              className="veri-select-field"
              value={veriBusinessProfile.veriBusinessType || 'sme'}
              onChange={(e) => veriHandleInputChange('veriBusinessType', e.target.value)}
            >
              {Object.entries(veriBusinessTypes).map(([key, labels]) => (
                <option key={key} value={key}>
                  {labels[veriLanguage === 'vietnamese' ? 'vi' : 'en']}
                </option>
              ))}
            </select>
          </div>
          
          <div className="veri-input-group">
            <label className="veri-input-label">
              {veriContent[veriLanguage].region}
            </label>
            <select
              className="veri-select-field"
              value={veriBusinessProfile.veriRegionalLocation || 'south'}
              onChange={(e) => veriHandleInputChange('veriRegionalLocation', e.target.value)}
            >
              {Object.entries(veriRegions).map(([key, labels]) => (
                <option key={key} value={key}>
                  {labels[veriLanguage === 'vietnamese' ? 'vi' : 'en']}
                </option>
              ))}
            </select>
          </div>
          
          <div className="veri-input-group">
            <label className="veri-input-label">
              {veriContent[veriLanguage].employees}
            </label>
            <input
              type="number"
              className="veri-input-field"
              value={veriBusinessProfile.veriEmployeeCount || 0}
              onChange={(e) => veriHandleInputChange('veriEmployeeCount', parseInt(e.target.value) || 0)}
              min="1"
              max="10000"
            />
          </div>
        </div>
      </form>

      <div className="veri-step-actions" style={{ marginTop: '32px' }}>
        <button 
          className="veri-secondary-button"
          onClick={veriGoBack}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            padding: '10px 20px',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            background: 'white',
            color: '#495057',
            border: '2px solid #ced4da',
            boxShadow: '0 2px 8px 0 rgba(0, 0, 0, 0.1)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            fontFamily: 'Inter, Segoe UI, system-ui, sans-serif',
            whiteSpace: 'nowrap'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#f8f9fa';
            e.currentTarget.style.borderColor = '#6b8e6b';
            e.currentTarget.style.color = '#6b8e6b';
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 4px 12px 0 rgba(0, 0, 0, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'white';
            e.currentTarget.style.borderColor = '#ced4da';
            e.currentTarget.style.color = '#495057';
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 2px 8px 0 rgba(0, 0, 0, 0.1)';
          }}
        >
          <span className="veri-button-icon" style={{ fontSize: '14px' }}>⬅️</span>
          {veriContent[veriLanguage].back}
        </button>
        
        <button 
          className="veri-primary-button"
          onClick={veriProceedToNext}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            padding: '10px 20px',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)',
            color: 'white',
            border: '2px solid rgba(107, 142, 107, 0.3)',
            boxShadow: '0 3px 10px 0 rgba(107, 142, 107, 0.4)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            fontFamily: 'Inter, Segoe UI, system-ui, sans-serif',
            whiteSpace: 'nowrap'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #8bb3d3 100%)';
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 5px 16px 0 rgba(107, 142, 107, 0.5)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)';
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 3px 10px 0 rgba(107, 142, 107, 0.4)';
          }}
        >
          <span className="veri-button-icon" style={{ fontSize: '14px' }}>➡️</span>
          {veriContent[veriLanguage].next}
        </button>
      </div>
    </div>
  );
};

export default VeriBusinessProfileSetupStep;