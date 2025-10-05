import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react';
// Types for Vietnamese Cultural Intelligence (will be imported from backend API)
interface VietnameseCulturalIntelligence {
  get_regional_context: (region: string) => any;
  get_sector_practices: (sector: string) => any;
  get_pdpl_cultural_guidance: (context: any) => any;
  validate_vietnamese_business_data: (data: any) => any;
  format_vietnamese_datetime: (date?: Date) => string;
}

enum VietnameseRegion {
  NORTH = 'northern_vietnam',
  SOUTH = 'southern_vietnam', 
  CENTRAL = 'central_vietnam'
}

enum BusinessSector {
  TECHNOLOGY = 'technology',
  MANUFACTURING = 'manufacturing',
  FINANCE = 'finance_banking',
  RETAIL = 'retail_commerce',
  HEALTHCARE = 'healthcare',
  EDUCATION = 'education'
}

/**
 * Custom hook for Vietnamese Cultural Intelligence integration with i18n
 * Provides culturally-aware translations based on business context
 */
export const useCulturalIntelligence = () => {
  const { t, i18n } = useTranslation(['common', 'cultural', 'vericompliance']);
  // Cultural AI integration via API calls to backend
  const culturalAI = {
    get_regional_context: async (region: string) => {
      // Will integrate with backend Vietnamese Cultural Intelligence API
      return { 
        region, 
        communication_style: 'formal_vietnamese',
        formality_level: 'high', 
        hierarchy_importance: 'important',
        businessContext: 'contextual_data' 
      };
    },
    get_sector_practices: async (sector: string) => {
      // Will integrate with backend API
      return { sector, practices: 'sector_data' };
    },
    get_pdpl_cultural_guidance: async (context: any) => {
      // Will integrate with backend API
      return { guidance: 'cultural_guidance', context };
    },
    validate_vietnamese_business_data: async (data: any) => {
      // Will integrate with backend API
      return { valid: true, data };
    },
    format_vietnamese_datetime: (date?: Date) => {
      return (date || new Date()).toLocaleString('vi-VN', {
        timeZone: 'Asia/Ho_Chi_Minh'
      });
    }
  };
  const [culturalContext, setCulturalContext] = useState<{
    region?: VietnameseRegion;
    sector?: BusinessSector;
    businessContext?: any;
  }>({});

  // Load cultural context from localStorage or default
  useEffect(() => {
    const savedContext = localStorage.getItem('verisyntra_cultural_context');
    if (savedContext) {
      try {
        const parsed = JSON.parse(savedContext);
        setCulturalContext(parsed);
      } catch (error) {
        console.warn('Failed to parse cultural context:', error);
      }
    }
  }, []);

  /**
   * Get culturally-aware translation based on Vietnamese business context
   */
  const tCultural = (
    key: string,
    options?: {
      region?: VietnameseRegion;
      sector?: BusinessSector;
      defaultValue?: string;
    }
  ) => {
    const { region, sector, defaultValue } = options || {};
    
    // Try to get region/sector specific translation first
    if (region || culturalContext.region) {
      const regionKey = `${key}_${region || culturalContext.region}`;
      const regionTranslation = t(regionKey, { defaultValue: null });
      if (regionTranslation !== regionKey) {
        return regionTranslation;
      }
    }
    
    if (sector || culturalContext.sector) {
      const sectorKey = `${key}_${sector || culturalContext.sector}`;
      const sectorTranslation = t(sectorKey, { defaultValue: null });
      if (sectorTranslation !== sectorKey) {
        return sectorTranslation;
      }
    }
    
    // Fall back to regular translation
    return t(key, { defaultValue });
  };

  /**
   * Get Vietnamese business context for current region/sector
   */
  const getBusinessContext = async () => {
    if (culturalContext.region) {
      return await culturalAI.get_regional_context(culturalContext.region);
    }
    return null;
  };

  /**
   * Get sector-specific practices
   */
  const getSectorPractices = async () => {
    if (culturalContext.sector) {
      return await culturalAI.get_sector_practices(culturalContext.sector);
    }
    return null;
  };

  /**
   * Update cultural context and translations
   */
  const updateCulturalContext = (context: {
    region?: VietnameseRegion;
    sector?: BusinessSector;
  }) => {
    const newContext = { ...culturalContext, ...context };
    setCulturalContext(newContext);
    localStorage.setItem('verisyntra_cultural_context', JSON.stringify(newContext));
    
    // Trigger re-render of translations with new context
    i18n.emit('languageChanged', i18n.language);
  };

  /**
   * Get PDPL compliance guidance with Vietnamese cultural context
   */
  const getPDPLGuidance = () => {
    return culturalAI.get_pdpl_cultural_guidance({
      region: culturalContext.region,
      sector: culturalContext.sector,
    });
  };

  /**
   * Validate Vietnamese business data with cultural context
   */
  const validateBusinessData = (data: Record<string, any>) => {
    return culturalAI.validate_vietnamese_business_data(data);
  };

  /**
   * Get appropriate communication style based on cultural context
   */
  const getCommunicationStyle = async () => {
    const businessContext = await getBusinessContext();
    if (businessContext) {
      return {
        style: businessContext.communication_style || 'formal_vietnamese',
        formality: businessContext.formality_level || 'high',
        hierarchy: businessContext.hierarchy_importance || 'important',
      };
    }
    return null;
  };

  /**
   * Format Vietnamese business datetime
   */
  const formatVietnameseDateTime = (date?: Date) => {
    return culturalAI.format_vietnamese_datetime(date);
  };

  return {
    t: tCultural,
    i18n,
    culturalContext,
    updateCulturalContext,
    getBusinessContext,
    getSectorPractices,
    getPDPLGuidance,
    validateBusinessData,
    getCommunicationStyle,
    formatVietnameseDateTime,
    culturalAI,
  };
};

/**
 * Hook for language switching with cultural intelligence
 */
export const useLanguageSwitch = () => {
  const { i18n } = useTranslation();
  const cultural = useCulturalIntelligence();

  const switchLanguage = (language: 'vi' | 'en') => {
    i18n.changeLanguage(language);
    
    // Log cultural intelligence context for analytics
    const context = cultural.getBusinessContext();
    if (context) {
      console.log(`Language switched to ${language} with cultural context:`, context);
    }
  };

  return {
    currentLanguage: i18n.language,
    switchLanguage,
    isVietnamese: i18n.language === 'vi',
    isEnglish: i18n.language === 'en',
  };
};

/**
 * Hook for Vietnamese regional business context
 */
export const useVietnameseRegion = (region: VietnameseRegion) => {
  const { t } = useTranslation('cultural');
  
  return {
    name: t(`regions.${region}.name`),
    businessCulture: t(`regions.${region}.businessCulture`),
    formalityLevel: t(`regions.${region}.formalityLevel`),
    hierarchyImportance: t(`regions.${region}.hierarchyImportance`),
    governmentProximity: t(`regions.${region}.governmentProximity`),
    communicationStyle: t(`regions.${region}.communicationStyle`),
    meetingPreferences: t(`regions.${region}.meetingPreferences`),
    decisionSpeed: t(`regions.${region}.decisionSpeed`),
    notes: t(`regions.${region}.notes`),
  };
};

/**
 * Hook for Vietnamese business sector context
 */
export const useBusinessSector = (sector: BusinessSector) => {
  const { t } = useTranslation('cultural');
  
  return {
    name: t(`sectors.${sector}.name`),
    meetingStyle: t(`sectors.${sector}.meetingStyle`),
    decisionSpeed: t(`sectors.${sector}.decisionSpeed`),
    complianceFocus: t(`sectors.${sector}.complianceFocus`),
    communication: t(`sectors.${sector}.communication`),
  };
};