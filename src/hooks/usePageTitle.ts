// Custom hook for managing page titles
// Dynamically updates browser tab title based on current page

import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface UsePageTitleOptions {
  title: string;
  titleVi?: string;
  includeAppName?: boolean;
}

export const usePageTitle = ({ 
  title, 
  titleVi, 
  includeAppName = true 
}: UsePageTitleOptions) => {
  const { i18n } = useTranslation();
  const isVietnamese = i18n.language === 'vi';

  useEffect(() => {
    const pageTitle = isVietnamese && titleVi ? titleVi : title;
    const fullTitle = includeAppName 
      ? `${pageTitle} | VeriSyntra`
      : pageTitle;
    
    document.title = fullTitle;

    // Cleanup: restore default title when component unmounts
    return () => {
      document.title = 'VeriSyntra - PDPL 2025 Compliance Platform';
    };
  }, [title, titleVi, includeAppName, isVietnamese]);
};
