import React, { useState, useEffect } from 'react';
import { Shield, CheckCircle, Globe, Server, Clock, Users } from 'lucide-react';
import axios from 'axios';

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
  const [language, setLanguage] = useState<'vi' | 'en'>('vi');
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

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'vi' ? 'en' : 'vi');
  };

  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-600';
      case 'disconnected': return 'text-red-600';
      default: return 'text-yellow-600';
    }
  };

  const getConnectionText = () => {
    if (language === 'vi') {
      switch (connectionStatus) {
        case 'connected': return 'Đã kết nối';
        case 'disconnected': return 'Mất kết nối';
        default: return 'Đang kết nối...';
      }
    } else {
      switch (connectionStatus) {
        case 'connected': return 'Connected';
        case 'disconnected': return 'Disconnected';
        default: return 'Connecting...';
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-teal-50 to-emerald-50">
      <header className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-teal-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">VeriSyntra</h1>
                <p className="text-sm text-gray-600">
                  {language === 'vi' ? 'Nền tảng tuân thủ PDPL 2025' : 'PDPL 2025 Compliance Platform'}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 ${getConnectionColor()}`}>
                <Server className="w-4 h-4" />
                <span className="text-sm font-medium">{getConnectionText()}</span>
              </div>
              
              <button
                onClick={toggleLanguage}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
              >
                <Globe className="w-4 h-4" />
                <span className="font-medium">{language === 'vi' ? 'Tiếng Việt' : 'English'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-emerald-600 rounded-xl flex items-center justify-center flex-shrink-0">
                <Shield className="w-7 h-7 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {language === 'vi' ? 'Chào mừng đến với VeriSyntra' : 'Welcome to VeriSyntra'}
                </h2>
                <p className="text-gray-600 mb-4">
                  {language === 'vi'
                    ? 'Giải pháp tuân thủ PDPL 2025 chuyên biệt cho doanh nghiệp Việt Nam với trí tuệ văn hóa tích hợp.'
                    : 'Specialized PDPL 2025 compliance solution for Vietnamese enterprises with integrated cultural intelligence.'
                  }
                </p>
                
                {backendData && (
                  <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 mb-4">
                    <h3 className="font-semibold text-emerald-900 mb-2">
                      {language === 'vi' ? 'Trạng thái hệ thống backend:' : 'Backend System Status:'}
                    </h3>
                    <p className="text-emerald-800 text-sm">
                      {language === 'vi' ? backendData.message : backendData.english}
                    </p>
                    <div className="mt-2 text-xs text-emerald-700">
                      <span className="font-medium">
                        {language === 'vi' ? 'Thời gian Việt Nam:' : 'Vietnam Time:'} 
                      </span> {backendData.vietnam_time}
                    </div>
                  </div>
                )}
                
                <div className="flex flex-wrap gap-2">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    PDPL 2025 {language === 'vi' ? 'Tuân thủ' : 'Compliant'}
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                    🇻🇳 {language === 'vi' ? 'Chuyên biệt Việt Nam' : 'Vietnam Specialized'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">
                {language === 'vi' ? 'Trí tuệ văn hóa Việt Nam' : 'Vietnamese Cultural AI'}
              </h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.cultural_ai === 'active' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.cultural_ai === 'active' 
                  ? (language === 'vi' ? 'Hoạt động' : 'Active')
                  : (language === 'vi' ? 'Không hoạt động' : 'Inactive')
                }
              </div>
              <p className="text-sm text-gray-600">
                {language === 'vi' 
                  ? 'Phân tích bối cảnh kinh doanh Việt Nam'
                  : 'Analyzing Vietnamese business context'
                }
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-teal-100 rounded-lg flex items-center justify-center">
                <Server className="w-5 h-5 text-teal-600" />
              </div>
              <h3 className="font-semibold text-gray-900">API Endpoints</h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.api_endpoints === 'operational' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.api_endpoints === 'operational' 
                  ? (language === 'vi' ? 'Hoạt động' : 'Operational')
                  : (language === 'vi' ? 'Không hoạt động' : 'Inactive')
                }
              </div>
              <p className="text-sm text-gray-600">
                {language === 'vi' ? 'Kết nối backend hoạt động tốt' : 'Backend connection working well'}
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                <Globe className="w-5 h-5 text-emerald-600" />
              </div>
              <h3 className="font-semibold text-gray-900">
                {language === 'vi' ? 'Cấu hình Việt Nam' : 'Vietnamese Locale'}
              </h3>
            </div>
            <div className="space-y-2">
              <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                systemStatus?.components.vietnamese_locale === 'configured' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {systemStatus?.components.vietnamese_locale === 'configured' 
                  ? (language === 'vi' ? 'Đã cấu hình' : 'Configured')
                  : (language === 'vi' ? 'Chưa cấu hình' : 'Not Configured')
                }
              </div>
              <p className="text-sm text-gray-600">
                {language === 'vi' ? 'Múi giờ và ngôn ngữ Việt Nam' : 'Vietnamese timezone and language'}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {language === 'vi' ? 'Hành động nhanh' : 'Quick Actions'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 hover:border-teal-300 hover:bg-teal-50 transition-colors">
              <Users className="w-5 h-5 text-teal-600" />
              <span className="font-medium text-gray-900">
                {language === 'vi' ? 'Quản lý người dùng' : 'User Management'}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 hover:border-orange-300 hover:bg-orange-50 transition-colors">
              <CheckCircle className="w-5 h-5 text-orange-600" />
              <span className="font-medium text-gray-900">
                {language === 'vi' ? 'Đánh giá tuân thủ' : 'Compliance Assessment'}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 transition-colors">
              <Shield className="w-5 h-5 text-emerald-600" />
              <span className="font-medium text-gray-900">
                {language === 'vi' ? 'Báo cáo PDPL' : 'PDPL Reports'}
              </span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors">
              <Clock className="w-5 h-5 text-blue-600" />
              <span className="font-medium text-gray-900">
                {language === 'vi' ? 'Lịch sử hoạt động' : 'Activity History'}
              </span>
            </button>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            {language === 'vi' 
              ? 'Phiên bản phát triển - Kết nối real-time với backend FastAPI'
              : 'Development Version - Real-time connection with FastAPI backend'
            }
          </p>
          <p className="mt-1">
            API Documentation: 
            <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer" 
               className="text-teal-600 hover:text-teal-700 ml-1">
              http://127.0.0.1:8000/docs
            </a>
          </p>
        </div>
      </main>
    </div>
  );
};

export default VeriSyntraApp;