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
      
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', marginTop: '32px' }}>
        {/* BACK BUTTON */}
        <button 
          onClick={() => veriOnPrevious('business-profile-setup')}
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
          <span style={{ fontSize: '14px' }}>⬅️</span>
          {t('common:navigation.back')}
        </button>
        
        {/* NEXT BUTTON */}
        <button 
          onClick={() => veriOnNext('cultural-preferences')}
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
          <span style={{ fontSize: '14px' }}>➡️</span>
          {t('common:navigation.next')}
        </button>
      </div>
    </div>
  );
};

export default VeriRegionalAdaptationStep;