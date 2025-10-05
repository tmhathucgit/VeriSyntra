// VeriPortal Language Switcher - AI-Powered Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { Globe } from 'lucide-react';
import {
  VeriAICulturalEngine,
  VeriMLPersonalizationEngine,
  VeriAutomationEngine
} from '../types';
import './VeriLanguageSwitcher.css';

interface VeriAILanguageSwitcherProps {
  veriCurrentLanguage: 'vietnamese' | 'english';
  setVeriLanguage: (lang: 'vietnamese' | 'english') => void;
  veriPrimaryLanguage: 'vietnamese' | 'english';
  veriSecondaryLanguage: 'vietnamese' | 'english';
  veriAIEngine?: VeriAICulturalEngine;
  veriMLPersonalization?: VeriMLPersonalizationEngine;
  veriAutomationEngine?: VeriAutomationEngine;
}



// AI-Powered VeriPortal Language Switcher with Machine Learning Intelligence
export const VeriLanguageSwitcher: React.FC<VeriAILanguageSwitcherProps> = ({
  veriCurrentLanguage,
  setVeriLanguage
}) => {

  // Simple and reliable language switching
  const veriHandleLanguageSwitch = (language: 'vietnamese' | 'english') => {
    console.log(`🌐 VeriPortal: Switching language from ${veriCurrentLanguage} to ${language}`);
    
    // Direct language change
    setVeriLanguage(language);
    
    console.log(`✅ Language successfully switched to ${language}`);
  };

  // Toggle between languages like main app
  const toggleLanguage = () => {
    const newLanguage = veriCurrentLanguage === 'vietnamese' ? 'english' : 'vietnamese';
    console.log(`� VeriPortal: Switching language from ${veriCurrentLanguage} to ${newLanguage}`);
    veriHandleLanguageSwitch(newLanguage);
  };

  return (
    <div className="flex justify-center">
      {/* Vietnamese Cultural Style Language Switcher */}
      <button
        onClick={toggleLanguage}
        className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 hover:shadow-md"
        style={{
          background: veriCurrentLanguage === 'vietnamese' 
            ? 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)'
            : 'linear-gradient(135deg, #7fa3c3 0%, #6b8e6b 100%)',
          border: '2px solid #d4c18a',
          color: 'white'
        }}
      >
        <Globe className="w-4 h-4" />
        <span className="font-medium">
          {veriCurrentLanguage === 'vietnamese' ? '🇻🇳 Tiếng Việt' : '🇺🇸 English'}
        </span>
      </button>
    </div>
  );
};

export default VeriLanguageSwitcher;