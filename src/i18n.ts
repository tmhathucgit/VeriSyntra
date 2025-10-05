import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Vietnamese translations
import commonVi from './locales/vi/common.json';
import veriportalVi from './locales/vi/veriportal.json';
import vericomplianceVi from './locales/vi/vericompliance.json';
import culturalVi from './locales/vi/cultural.json';

// English translations  
import commonEn from './locales/en/common.json';
import veriportalEn from './locales/en/veriportal.json';
import vericomplianceEn from './locales/en/vericompliance.json';
import culturalEn from './locales/en/cultural.json';

const resources = {
  vi: {
    common: commonVi,
    veriportal: veriportalVi,
    vericompliance: vericomplianceVi,
    cultural: culturalVi,
  },
  en: {
    common: commonEn,
    veriportal: veriportalEn,
    vericompliance: vericomplianceEn,
    cultural: culturalEn,
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'vi', // Default to Vietnamese as per requirements
    fallbackLng: 'vi', // Fallback to Vietnamese, not English
    
    // Vietnamese Cultural Intelligence Integration
    contextSeparator: '_',
    pluralSeparator: '_',
    
    // Namespace configuration for microservices
    defaultNS: 'common',
    ns: ['common', 'veriportal', 'vericompliance', 'cultural'],
    
    interpolation: {
      escapeValue: false, // React already does escaping
    },
    
    // Vietnamese locale settings
    parseMissingKeyHandler: (key) => {
      console.warn(`Missing translation key: ${key}`);
      return key;
    },
    
    // Development settings
    debug: process.env.NODE_ENV === 'development',
    
    // Vietnamese business hours and cultural context
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
    
    // Cultural intelligence integration options
    react: {
      useSuspense: false,
      bindI18n: 'languageChanged',
      bindI18nStore: 'added removed',
      transEmptyNodeValue: '',
      transSupportBasicHtmlNodes: true,
      transKeepBasicHtmlNodesFor: ['br', 'strong', 'i', 'em'],
    }
  });

// Vietnamese Cultural Intelligence Hook Integration
export const getCulturalContext = (region?: string, sector?: string) => {
  const context: Record<string, string> = {};
  
  if (region) {
    context.region = region;
  }
  
  if (sector) {
    context.sector = sector;
  }
  
  return context;
};

// Vietnamese business time utilities
export const getVietnameseBusinessTime = () => {
  return new Date().toLocaleString('vi-VN', {
    timeZone: 'Asia/Ho_Chi_Minh',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};

// Export for cultural intelligence integration
export const setLanguageWithCulturalContext = (
  language: string, 
  culturalContext?: { region?: string; sector?: string }
) => {
  i18n.changeLanguage(language);
  
  // Store cultural context for Vietnamese Cultural Intelligence integration
  if (culturalContext) {
    localStorage.setItem('verisyntra_cultural_context', JSON.stringify(culturalContext));
  }
};

export default i18n;