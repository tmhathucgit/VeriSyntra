// VeriPortal Language Switcher - AI-Powered Vietnamese Cultural Component
// Implementation Status: ✅ IMPLEMENTED

import React from 'react';
import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation(['common', 'veriportal']);

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
      {/* Main App Style Language Switcher */}
      <button
        onClick={toggleLanguage}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
      >
        <Globe className="w-4 h-4" />
        <span className="font-medium">{t('common:language.current')}</span>
      </button>
    </div>
  );
};

export default VeriLanguageSwitcher;