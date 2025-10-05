// VeriPortal Compliance Readiness Step - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { VeriOnboardingStep } from '../../types';

interface VeriComplianceReadinessStepProps {
  veriLanguage: 'vietnamese' | 'english';
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriComplianceReadinessStep: React.FC<VeriComplianceReadinessStepProps> = ({
  veriLanguage,
  veriOnNext,
  veriOnPrevious
}) => {
  return (
    <div>
      <h2>{veriLanguage === 'vietnamese' ? 'Sẵn sàng Tuân thủ' : 'Compliance Readiness'}</h2>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', marginTop: '32px' }}>
        {/* BACK BUTTON */}
        <button 
          onClick={() => veriOnPrevious('cultural-preferences')}
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
          {veriLanguage === 'vietnamese' ? 'Quay lại' : 'Back'}
        </button>
        
        {/* NEXT BUTTON */}
        <button 
          onClick={() => veriOnNext('completion-summary')}
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
          {veriLanguage === 'vietnamese' ? 'Tiếp tục' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default VeriComplianceReadinessStep;