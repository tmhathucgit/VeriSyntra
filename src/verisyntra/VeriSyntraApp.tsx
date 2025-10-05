import React, { useEffect } from 'react';
import { Shield, CheckCircle, Clock, Users, Server, Globe } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { useLanguageSwitch } from '../hooks/useCulturalIntelligence';
import { useState } from 'react';
import { VeriSyntraBanner } from '../components/shared/VeriSyntraBanner';

interface SystemStatus {
  status: string;
  service: string;
  timestamp: string;
  components: {
    cultural_ai: string;
    api_endpoints: string;
    vietnamese_locale: string;
  };
}

interface ApiResponse {
  message: string;
  english: string;
  status: string;
  vietnam_time: string;
  cultural_context: string;
}

const VeriSyntraApp: React.FC = () => {
  const { t } = useTranslation(['common', 'vericompliance']);
  const { switchLanguage, isVietnamese } = useLanguageSwitch();
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [backendData, setBackendData] = useState<ApiResponse | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');

  useEffect(() => {
    const testBackendConnection = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/');
        setBackendData(response.data);
        setConnectionStatus('connected');
      } catch (error) {
        console.error('Backend connection failed:', error);
        setConnectionStatus('disconnected');
      }
    };

    const fetchSystemStatus = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/health');
        setSystemStatus(response.data);
      } catch (error) {
        console.error('Health check failed:', error);
      }
    };

    testBackendConnection();
    fetchSystemStatus();

    const interval = setInterval(() => {
      testBackendConnection();
      fetchSystemStatus();
    }, 30000);

    return () => clearInterval(interval);
  }, []);



  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-green-50" style={{
      background: 'linear-gradient(135deg, #f0f4f0 0%, #f1f6fb 25%, #f0f4f0 50%, #f1f6fb 75%, #f0f4f0 100%)'
    }}>
      <VeriSyntraBanner
        variant="main"
        currentLanguage={isVietnamese ? 'vi' : 'en'}
        onLanguageChange={(lang) => switchLanguage(lang)}
        showConnectionStatus={true}
        showLanguageToggle={true}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6 border-2" style={{
            borderColor: '#d4c18a',
            boxShadow: '0 8px 32px rgba(107, 142, 107, 0.15)'
          }}>
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0" style={{
                background: 'linear-gradient(145deg, #6b8e6b, #7fa3c3)',
                boxShadow: '0 4px 16px rgba(107, 142, 107, 0.3)'
              }}>
                <Shield className="w-7 h-7 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {t('common:welcome.title')}
                </h2>
                <p className="text-gray-600 mb-4">
                  {t('common:welcome.description')}
                </p>
                
                {backendData && (
                  <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 mb-4">
                    <h3 className="font-semibold text-emerald-900 mb-2">
                      {t('common:system.backendStatus')}
                    </h3>
                    <p className="text-emerald-800 text-sm">
                      {isVietnamese ? backendData.message : backendData.english}
                    </p>
                    <div className="mt-2 text-xs text-emerald-700">
                      <span className="font-medium">
                        {t('common:system.vietnamTime')} 
                      </span> {backendData.vietnam_time}
                    </div>
                  </div>
                )}
                
                <div className="flex flex-wrap gap-2">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium" style={{
                    backgroundColor: '#f0f8f0',
                    color: '#6b8e6b',
                    border: '1px solid #6b8e6b'
                  }}>
                    <CheckCircle className="w-4 h-4 mr-1" />
                    {t('vericompliance:badges.pdplCompliant')}
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium" style={{
                    backgroundColor: '#f8f4f0',
                    color: '#c17a7a',
                    border: '1px solid #d4c18a'
                  }}>
                    🇻🇳 {t('vericompliance:badges.vietnamSpecialized')}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border-2" style={{
            borderColor: '#d4c18a',
            boxShadow: '0 4px 16px rgba(107, 142, 107, 0.1)'
          }}>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{
                background: 'linear-gradient(145deg, #6b8e6b, #7fa088)',
                boxShadow: '0 2px 8px rgba(107, 142, 107, 0.25)'
              }}>
                <Shield className="w-5 h-5 text-white" />
              </div>
              <h3 className="font-semibold" style={{ color: '#6b8e6b' }}>
                {t('common:features.culturalAI')}
              </h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.cultural_ai === 'active' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.cultural_ai === 'active' 
                  ? t('common:status.active')
                  : t('common:status.inactive')
                }
              </div>
              <p className="text-sm text-gray-600">
                {t('common:features.businessContextAnalysis')}
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border-2" style={{
            borderColor: '#d4c18a',
            boxShadow: '0 4px 16px rgba(127, 163, 195, 0.1)'
          }}>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{
                background: 'linear-gradient(145deg, #7fa3c3, #6b8e6b)',
                boxShadow: '0 2px 8px rgba(127, 163, 195, 0.25)'
              }}>
                <Server className="w-5 h-5 text-white" />
              </div>
              <h3 className="font-semibold" style={{ color: '#7fa3c3' }}>API Endpoints</h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.api_endpoints === 'operational' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.api_endpoints === 'operational' 
                  ? t('common:status.operational')
                  : t('common:status.inactive')
                }
              </div>
              <p className="text-sm text-gray-600">
                {t('common:system.backendConnection')}
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border-2" style={{
            borderColor: '#d4c18a',
            boxShadow: '0 4px 16px rgba(107, 142, 107, 0.1)'
          }}>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{
                background: 'linear-gradient(145deg, #c17a7a, #d4c18a)',
                boxShadow: '0 2px 8px rgba(193, 122, 122, 0.25)'
              }}>
                <Globe className="w-5 h-5 text-white" />
              </div>
              <h3 className="font-semibold" style={{ color: '#c17a7a' }}>
                {t('common:system.vietnameseLocale')}
              </h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.vietnamese_locale === 'configured' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.vietnamese_locale === 'configured' 
                  ? t('common:status.configured')
                  : t('common:status.notConfigured')
                }
              </div>
              <p className="text-sm text-gray-600">
                {t('common:system.timezoneLanguage')}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border-2" style={{
          borderColor: '#d4c18a',
          boxShadow: '0 8px 32px rgba(107, 142, 107, 0.15)'
        }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: '#6b8e6b' }}>
            {t('common:quickActions.title')}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="flex items-center space-x-3 p-4 rounded-lg border-2 transition-all duration-300 hover:shadow-lg" style={{
              borderColor: '#d4c18a',
              backgroundColor: 'rgba(107, 142, 107, 0.05)'
            }} onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(107, 142, 107, 0.1)';
              e.currentTarget.style.borderColor = '#6b8e6b';
            }} onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(107, 142, 107, 0.05)';
              e.currentTarget.style.borderColor = '#d4c18a';
            }}>
              <Users className="w-5 h-5" style={{ color: '#6b8e6b' }} />
              <span className="font-medium" style={{ color: '#6b8e6b' }}>
                {t('common:quickActions.userManagement')}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border-2 transition-all duration-300 hover:shadow-lg" style={{
              borderColor: '#d4c18a',
              backgroundColor: 'rgba(127, 163, 195, 0.05)'
            }} onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(127, 163, 195, 0.1)';
              e.currentTarget.style.borderColor = '#7fa3c3';
            }} onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(127, 163, 195, 0.05)';
              e.currentTarget.style.borderColor = '#d4c18a';
            }}>
              <CheckCircle className="w-5 h-5" style={{ color: '#7fa3c3' }} />
              <span className="font-medium" style={{ color: '#7fa3c3' }}>
                {t('common:quickActions.complianceAssessment')}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border-2 transition-all duration-300 hover:shadow-lg" style={{
              borderColor: '#d4c18a',
              backgroundColor: 'rgba(193, 122, 122, 0.05)'
            }} onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(193, 122, 122, 0.1)';
              e.currentTarget.style.borderColor = '#c17a7a';
            }} onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(193, 122, 122, 0.05)';
              e.currentTarget.style.borderColor = '#d4c18a';
            }}>
              <Shield className="w-5 h-5" style={{ color: '#c17a7a' }} />
              <span className="font-medium" style={{ color: '#c17a7a' }}>
                {t('common:quickActions.pdplReports')}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border-2 transition-all duration-300 hover:shadow-lg" style={{
              borderColor: '#d4c18a',
              backgroundColor: 'rgba(212, 193, 138, 0.05)'
            }} onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(212, 193, 138, 0.1)';
              e.currentTarget.style.borderColor = '#d4c18a';
            }} onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(212, 193, 138, 0.05)';
              e.currentTarget.style.borderColor = '#d4c18a';
            }}>
              <Clock className="w-5 h-5" style={{ color: '#d4c18a' }} />
              <span className="font-medium" style={{ color: '#d4c18a' }}>
                {t('common:quickActions.activityHistory')}
              </span>
            </button>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            {t('common:footer.developmentVersion')}
          </p>
          <p className="mt-1">
            API Documentation: 
            <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer" 
               className="ml-1 font-medium transition-colors duration-300"
               style={{ color: '#7fa3c3' }}
               onMouseEnter={(e) => (e.currentTarget as HTMLAnchorElement).style.color = '#6b8e6b'}
               onMouseLeave={(e) => (e.currentTarget as HTMLAnchorElement).style.color = '#7fa3c3'}>
              http://127.0.0.1:8000/docs
            </a>
          </p>
        </div>
      </main>
    </div>
  );
};

export default VeriSyntraApp;