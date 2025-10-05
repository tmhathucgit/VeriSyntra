// VeriSyntra Shared Banner Component
// Reusable banner component for consistent branding across VeriSyntra applications

import React, { useState, useEffect } from 'react';
import { Server, Globe } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import axios from 'axios';
import vnMapLogo from '../../../svg/vnMapLogo.svg';

interface VeriSyntraBannerProps {
  showConnectionStatus?: boolean;
  showLanguageToggle?: boolean;
  customTitle?: string;
  customSubtitle?: string;
  onLanguageChange?: (language: 'vi' | 'en') => void;
  currentLanguage?: 'vi' | 'en';
  variant?: 'main' | 'portal' | 'compact';
}

export const VeriSyntraBanner: React.FC<VeriSyntraBannerProps> = ({
  showConnectionStatus = true,
  showLanguageToggle = true,
  customTitle,
  customSubtitle,
  onLanguageChange,
  currentLanguage = 'vi',
  variant = 'main'
}) => {
  const { t, i18n } = useTranslation(['common', 'vericompliance']);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');

  const isVietnamese = currentLanguage === 'vi' || i18n.language === 'vi';

  useEffect(() => {
    if (!showConnectionStatus) return;

    const testBackendConnection = async () => {
      try {
        await axios.get('http://127.0.0.1:8000/');
        setConnectionStatus('connected');
      } catch (error) {
        console.error('Backend connection failed:', error);
        setConnectionStatus('disconnected');
      }
    };

    testBackendConnection();

    const interval = setInterval(() => {
      testBackendConnection();
    }, 30000);

    return () => clearInterval(interval);
  }, [showConnectionStatus]);

  const toggleLanguage = () => {
    const newLanguage = isVietnamese ? 'en' : 'vi';
    if (onLanguageChange) {
      onLanguageChange(newLanguage);
    } else {
      i18n.changeLanguage(newLanguage);
    }
  };

  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-600';
      case 'disconnected': return 'text-red-600';
      default: return 'text-yellow-600';
    }
  };

  const getConnectionText = () => {
    if (isVietnamese) {
      switch (connectionStatus) {
        case 'connected': return t('common:status.connected');
        case 'disconnected': return t('common:status.disconnected');
        default: return t('common:status.connecting');
      }
    } else {
      switch (connectionStatus) {
        case 'connected': return t('common:status.connected');
        case 'disconnected': return t('common:status.disconnected');
        default: return t('common:status.connecting');
      }
    }
  };

  const getBannerStyle = () => {
    switch (variant) {
      case 'portal':
        return {
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(12px)',
          borderBottom: '2px solid #c17a7a',
          boxShadow: '0 4px 20px rgba(107, 142, 107, 0.1)'
        };
      case 'compact':
        return {
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(8px)',
          borderBottom: '1px solid #d4c18a'
        };
      default:
        return {
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(8px)',
          borderBottom: '2px solid #c17a7a'
        };
    }
  };

  const getLogoSize = () => {
    switch (variant) {
      case 'compact': return 'w-8 h-8';
      default: return 'w-12 h-12';
    }
  };

  const getTitleSize = () => {
    switch (variant) {
      case 'compact': return 'text-lg';
      default: return 'text-xl';
    }
  };

  return (
    <header 
      className="sticky top-0 z-50"
      style={getBannerStyle()}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className={`flex justify-between items-center ${variant === 'compact' ? 'h-12' : 'h-16'}`}>
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div className={`${getLogoSize()} rounded-lg p-1 bg-white/95 backdrop-blur-sm`} style={{
              border: '1px solid #d4c18a',
              boxShadow: '0 2px 8px rgba(212, 193, 138, 0.15)'
            }}>
              <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-full h-full" />
            </div>
            <div>
              <h1 className={`${getTitleSize()} font-bold`} style={{ color: '#6b8e6b' }}>
                {customTitle || 'VeriSyntra'}
              </h1>
              {variant !== 'compact' && (
                <p className="text-sm" style={{ color: '#7fa3c3' }}>
                  {customSubtitle || t('vericompliance:platform.title')}
                </p>
              )}
            </div>
          </Link>

          <div className="flex items-center space-x-4">
            {showConnectionStatus && (
              <div className={`flex items-center space-x-2 ${getConnectionColor()}`}>
                <Server className="w-4 h-4" />
                <span className="text-sm font-medium">{getConnectionText()}</span>
              </div>
            )}
            
            {showLanguageToggle && (
              <button
                onClick={toggleLanguage}
                className="flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 hover:shadow-md"
                style={{
                  background: isVietnamese 
                    ? 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)'
                    : 'linear-gradient(135deg, #7fa3c3 0%, #6b8e6b 100%)',
                  border: '2px solid #d4c18a',
                  color: 'white'
                }}
              >
                <Globe className="w-4 h-4" />
                <span className="font-medium">
                  {isVietnamese ? '🇻🇳 Tiếng Việt' : '🇺🇸 English'}
                </span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default VeriSyntraBanner;