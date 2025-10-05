// VeriPortal Layout with Landing Page Theme Integration
// Implementation Status: 🚀 UPDATED WITH COMPLIANCE WIZARDS

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowLeft, Shield, Star, FileText, GraduationCap, BarChart3, Smartphone, Network } from 'lucide-react';
import vnMapLogo from '../../../svg/vnMapLogo.svg';
import { VeriLanguageSwitcher } from './CulturalOnboarding/components';
import { VeriCulturalOnboardingSystem } from './CulturalOnboarding/VeriCulturalOnboardingSystem';
import { VeriComplianceWizardSystem } from './ComplianceWizards';
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
    <div className="min-h-screen" style={{
      background: 'linear-gradient(135deg, #f0f4f0 0%, #f1f6fb 25%, #f0f4f0 50%, #f1f6fb 75%, #f0f4f0 100%)'
    }}>
      {/* Navigation Bar - Vietnamese Cultural Style */}
      <nav className="fixed w-full bg-white/95 backdrop-blur-sm z-50 border-b-2" style={{
        borderColor: '#c17a7a'
      }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo - Vietnamese Cultural Style */}
            <Link to="/" className="flex items-center group">
              <div className="flex items-center space-x-2 group-hover:scale-105 transition-transform">
                <div className="w-10 h-10 rounded-lg p-1 bg-white/95 backdrop-blur-sm" style={{
                  border: '1px solid #d4c18a',
                  boxShadow: '0 2px 8px rgba(212, 193, 138, 0.15)'
                }}>
                  <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-full h-full" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xl font-bold" style={{ color: '#6b8e6b' }}>VeriSyntra</span>
                  <span className="text-xs font-medium" style={{ 
                    color: '#7fa3c3',
                    letterSpacing: '0.5px'
                  }}>
                    {isVietnamese ? 'Nền tảng Tuân thủ PDPL 2025' : 'PDPL 2025 Compliance Platform'}
                  </span>
                </div>
              </div>
            </Link>

            {/* VeriPortal Banner - Vietnamese Cultural Style */}
            <div className="hidden md:flex items-center space-x-4">
              <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full text-sm font-medium shadow-lg" style={{
                background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #c17a7a 100%)',
                color: 'white',
                border: '1px solid #d4c18a'
              }}>
                <Shield size={16} />
                <span className="flex items-center gap-1">
                  🇻🇳 {isVietnamese ? 'Chào mừng đến VeriSyntra' : 'Welcome to VeriSyntra'}
                </span>
              </div>
            </div>

            {/* Navigation Actions - Vietnamese Cultural Style */}
            <div className="flex items-center space-x-4">
              <Link 
                to="/" 
                className="flex items-center space-x-2 text-sm font-medium transition-colors" 
                style={{ color: '#7fa3c3' }}
                onMouseEnter={(e) => (e.currentTarget as HTMLAnchorElement).style.color = '#6b8e6b'}
                onMouseLeave={(e) => (e.currentTarget as HTMLAnchorElement).style.color = '#7fa3c3'}
              >
                <ArrowLeft size={16} />
                <span>{isVietnamese ? 'Quay lại' : 'Back to Home'}</span>
              </Link>
              <Link 
                to="/app" 
                className="px-4 py-2 rounded-lg font-medium transition-all transform hover:scale-105 shadow-sm"
                style={{
                  background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)',
                  color: 'white',
                  border: '1px solid #d4c18a'
                }}
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

        {/* Mobile VeriPortal Banner - Vietnamese Cultural Style */}
        <div className="md:hidden border-t text-white" style={{
          borderColor: '#d4c18a',
          background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #c17a7a 100%)'
        }}>
          <div className="px-4 py-3 text-center">
            <span className="flex items-center justify-center gap-2 text-sm font-medium">
              🇻🇳 {isVietnamese ? 'Chào mừng đến VeriSyntra' : 'Welcome to VeriSyntra'}
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="pt-24 md:pt-20 min-h-screen">
        {/* Vietnamese Cultural Background Pattern */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full opacity-5 transform rotate-12" style={{
            background: 'radial-gradient(circle, rgba(107, 142, 107, 0.3) 0%, rgba(127, 163, 195, 0.2) 100%)'
          }}></div>
          <div className="absolute bottom-1/4 right-1/4 w-48 h-48 rounded-full opacity-5 transform -rotate-12" style={{
            background: 'radial-gradient(circle, rgba(193, 122, 122, 0.3) 0%, rgba(212, 193, 138, 0.2) 100%)'
          }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full opacity-3" style={{
            background: 'radial-gradient(circle, rgba(127, 163, 195, 0.2) 0%, rgba(107, 142, 107, 0.1) 100%)'
          }}></div>
        </div>

        {/* Content Container */}
        <div className="relative z-10">
          {children}
        </div>
      </main>

      {/* Footer - Vietnamese Cultural Pride Section */}
      <footer className="relative z-10 bg-white/90 backdrop-blur-sm border-t-2 mt-auto" style={{
        borderColor: '#d4c18a'
      }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-3">
              <div className="w-6 h-6 rounded bg-white/95 backdrop-blur-sm p-0.5" style={{
                border: '1px solid #d4c18a'
              }}>
                <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-full h-full" />
              </div>
              <span className="text-sm font-medium" style={{ color: '#6b8e6b' }}>
                🇻🇳 {isVietnamese ? 'Tự hào phục vụ doanh nghiệp Việt Nam' : 'Proudly serving Vietnamese businesses'}
              </span>
            </div>
            <div className="flex items-center space-x-6 text-sm" style={{ color: '#7fa3c3' }}>
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