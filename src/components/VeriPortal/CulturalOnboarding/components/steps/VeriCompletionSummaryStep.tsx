// VeriPortal Completion Summary Step - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { VeriOnboardingStep } from '../../types';

interface VeriCompletionSummaryStepProps {
  veriLanguage: 'vietnamese' | 'english';
  veriOnNext: (nextStep: VeriOnboardingStep) => void;
  veriOnPrevious: (prevStep: VeriOnboardingStep) => void;
}

export const VeriCompletionSummaryStep: React.FC<VeriCompletionSummaryStepProps> = ({
  veriLanguage,
  veriOnPrevious
}) => {
  const navigate = useNavigate();
  const [showCompletionModal, setShowCompletionModal] = useState(false);

  const handleFinish = () => {
    setShowCompletionModal(true);
  };

  const handleCloseAndRedirect = () => {
    // Close modal first
    setShowCompletionModal(false);
    // Redirect to Compliance Wizards after a short delay for smooth transition
    setTimeout(() => {
      navigate('/veriportal');
    }, 300);
  };

  return (
    <div>
      <h2>{veriLanguage === 'vietnamese' ? 'Tóm tắt Hoàn thành' : 'Completion Summary'}</h2>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', marginTop: '32px' }}>
        {/* BACK BUTTON */}
        <button 
          onClick={() => veriOnPrevious('compliance-readiness')}
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
        
        {/* FINISH BUTTON - Special celebration styling */}
        <button 
          onClick={handleFinish}
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
            background: 'linear-gradient(135deg, #6b8e6b 0%, #d4c18a 100%)',
            color: 'white',
            border: '2px solid rgba(212, 193, 138, 0.4)',
            boxShadow: '0 3px 12px 0 rgba(212, 193, 138, 0.5)',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            fontFamily: 'Inter, Segoe UI, system-ui, sans-serif',
            whiteSpace: 'nowrap'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #dcc898 100%)';
            e.currentTarget.style.transform = 'translateY(-2px) scale(1.02)';
            e.currentTarget.style.boxShadow = '0 5px 18px 0 rgba(212, 193, 138, 0.6)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #d4c18a 100%)';
            e.currentTarget.style.transform = 'translateY(0) scale(1)';
            e.currentTarget.style.boxShadow = '0 3px 12px 0 rgba(212, 193, 138, 0.5)';
          }}
        >
          <span style={{ fontSize: '14px' }}>🎉</span>
          {veriLanguage === 'vietnamese' ? 'Hoàn thành' : 'Finish'}
        </button>
      </div>

      {/* CUSTOM COMPLETION MODAL - Replaces browser alert */}
      {showCompletionModal && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999
          }}
          onClick={() => setShowCompletionModal(false)}
        >
          <div 
            style={{
              background: 'white',
              borderRadius: '10px',
              padding: '16px',
              maxWidth: '280px',
              maxHeight: '70vh',
              overflow: 'auto',
              boxShadow: '0 8px 30px rgba(0, 0, 0, 0.2)',
              textAlign: 'center'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ fontSize: '18px', marginBottom: '8px' }}>🎉</div>
            <h3 style={{ 
              fontSize: '16px', 
              fontWeight: '700', 
              marginBottom: '6px',
              background: 'linear-gradient(135deg, #6b8e6b 0%, #d4c18a 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>
              {veriLanguage === 'vietnamese' ? 'Đã hoàn thành!' : 'Completed!'}
            </h3>
            <p style={{ 
              color: '#6c757d', 
              marginBottom: '14px',
              fontSize: '11px',
              lineHeight: '1.4'
            }}>
              {veriLanguage === 'vietnamese' 
                ? 'Bạn đã hoàn thành thành công quá trình giới thiệu văn hóa.'
                : 'You have successfully completed the cultural onboarding process.'}
            </p>
            <button
              onClick={handleCloseAndRedirect}
              style={{
                background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                padding: '7px 18px',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                boxShadow: '0 2px 6px rgba(107, 142, 107, 0.3)',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #8bb3d3 100%)';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(107, 142, 107, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 2px 8px rgba(107, 142, 107, 0.3)';
              }}
            >
              {veriLanguage === 'vietnamese' ? 'Đóng' : 'Close'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VeriCompletionSummaryStep;