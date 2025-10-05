// VeriPortal Layout with Landing Page Theme Integration
// Implementation Status: 🚀 NEW IMPLEMENTATION

import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Shield } from 'lucide-react';
import vnMapLogo from '../../../svg/vnMapLogo.svg';
import { VeriLanguageSwitcher } from './CulturalOnboarding/components';
import './VeriPortalTheme.css';

interface VeriPortalLayoutProps {
  children: React.ReactNode;
  veriLanguage?: 'vietnamese' | 'english';
  veriCurrentLanguage?: 'vietnamese' | 'english';
  setVeriLanguage?: (lang: 'vietnamese' | 'english') => void;
}

export const VeriPortalLayout: React.FC<VeriPortalLayoutProps> = ({
  children,
  veriLanguage = 'vietnamese',
  veriCurrentLanguage,
  setVeriLanguage
}) => {
  const { t, i18n } = useTranslation(['common', 'veriportal']);
  // Use i18n language state as primary source of truth, fallback to prop
  const isVietnamese = i18n.language === 'vi' || veriLanguage === 'vietnamese';

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-teal-50 to-emerald-50">
      {/* Navigation Bar - Same as Landing Page */}
      <nav className="fixed w-full bg-white/95 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo - Same as Landing */}
            <Link to="/" className="flex items-center group">
              <div className="flex items-center space-x-0 group-hover:scale-105 transition-transform">
                <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-8 h-8" />
                <span className="text-xl font-bold text-slate-800">VeriSyntra</span>
              </div>
            </Link>

            {/* VeriPortal Banner */}
            <div className="hidden md:flex items-center space-x-4">
              <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-red-600 via-yellow-500 to-red-600 text-white px-4 py-2 rounded-full text-sm font-medium shadow-lg">
                <Shield size={16} />
                <span className="flex items-center gap-1">
                  🇻🇳 {isVietnamese ? 'VeriPortal - Onboarding Văn hóa Việt' : 'VeriPortal - Vietnamese Cultural Onboarding'}
                </span>
              </div>
            </div>

            {/* Navigation Actions */}
            <div className="flex items-center space-x-4">
              <Link 
                to="/" 
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
              >
                <ArrowLeft size={16} />
                <span>{isVietnamese ? 'Quay lại' : 'Back to Home'}</span>
              </Link>
              <Link 
                to="/app" 
                className="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg font-medium transition-all transform hover:scale-105 shadow-sm"
              >
                {t('veriportal:hero.enterApp')}
              </Link>
              
              {/* Language Switcher */}
              {veriCurrentLanguage && setVeriLanguage && (
                <VeriLanguageSwitcher
                  veriCurrentLanguage={veriCurrentLanguage}
                  setVeriLanguage={setVeriLanguage}
                  veriPrimaryLanguage="vietnamese"
                  veriSecondaryLanguage="english"
                />
              )}
            </div>
          </div>
        </div>

        {/* Mobile VeriPortal Banner */}
        <div className="md:hidden border-t border-gray-100 bg-gradient-to-r from-red-600 via-yellow-500 to-red-600 text-white">
          <div className="px-4 py-3 text-center">
            <span className="flex items-center justify-center gap-2 text-sm font-medium">
              🇻🇳 {isVietnamese ? 'VeriPortal - Onboarding Văn hóa Việt' : 'VeriPortal - Vietnamese Cultural Onboarding'}
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="pt-24 md:pt-20 min-h-screen">
        {/* Hero Section Background Pattern - Similar to Landing */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-tr from-orange-200 to-emerald-300 rounded-full opacity-10 transform rotate-12"></div>
          <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-gradient-to-tr from-teal-200 to-orange-300 rounded-full opacity-10 transform -rotate-12"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-tr from-emerald-200 to-teal-300 rounded-full opacity-5"></div>
        </div>

        {/* Content Container */}
        <div className="relative z-10">
          {children}
        </div>
      </main>

      {/* Footer - Vietnamese Pride Section */}
      <footer className="relative z-10 bg-white/80 backdrop-blur-sm border-t border-gray-100 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-3">
              <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-6 h-6" />
              <span className="text-gray-600 text-sm">
                🇻🇳 {isVietnamese ? 'Tự hào phục vụ doanh nghiệp Việt Nam' : 'Proudly serving Vietnamese businesses'}
              </span>
            </div>
            <div className="flex items-center space-x-6 text-sm text-gray-500">
              <span>{isVietnamese ? 'Tuân thủ PDPL 2025' : 'PDPL 2025 Compliance'}</span>
              <span className="flex items-center gap-1">
                <Shield size={14} />
                {isVietnamese ? 'Bảo mật dữ liệu' : 'Data Security'}
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default VeriPortalLayout;