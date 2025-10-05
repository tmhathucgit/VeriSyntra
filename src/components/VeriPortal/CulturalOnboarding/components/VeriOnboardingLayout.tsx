// VeriPortal Onboarding Layout - Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import './VeriOnboardingLayout.css';

interface VeriOnboardingLayoutProps {
  children: React.ReactNode;
  veriCulturalStyle?: 'north' | 'central' | 'south';
}

export const VeriOnboardingLayout: React.FC<VeriOnboardingLayoutProps> = ({
  children,
  veriCulturalStyle = 'south'
}) => {
  return (
    <div 
      className={`veri-onboarding-layout veri-cultural-${veriCulturalStyle}`}
      data-cultural-region={veriCulturalStyle}
    >
      <div className="veri-layout-background">
        <div className="veri-cultural-pattern veri-pattern-1"></div>
        <div className="veri-cultural-pattern veri-pattern-2"></div>
        <div className="veri-cultural-pattern veri-pattern-3"></div>
      </div>
      
      <div className="veri-layout-content">
        {children}
      </div>
      
      <div className="veri-cultural-footer">
        <div className="veri-vietnam-pride">
          <span className="veri-flag">🇻🇳</span>
          <span>Tự hào phục vụ doanh nghiệp Việt Nam</span>
        </div>
      </div>
    </div>
  );
};

export default VeriOnboardingLayout;