// Vietnamese Training Integration System - Main Export File
// Comprehensive AI-powered PDPL 2025 Training & Education System

// Main Vietnamese Training Integration System Component
export { default as VeriTrainingIntegrationSystem } from './components/VeriTrainingIntegrationSystem';

// Vietnamese Training Integration Types
export * from './types';
export * from './extendedTypes';

// Vietnamese Training AI Services
export { veriTrainingAIEngine } from './services/veriTrainingAIService';

// Vietnamese Training Integration Styles (CSS import for bundlers that support it)
import './styles/veriTrainingStyles.css';

// Vietnamese Training Integration System Information
export const VeriTrainingIntegrationInfo = {
  systemName: 'VeriSyntra Training Integration',
  systemNameVi: 'Tích Hợp Đào Tạo VeriSyntra',
  version: '1.0.0',
  description: 'Comprehensive AI-powered PDPL 2025 Training & Education System with Vietnamese cultural intelligence',
  descriptionVi: 'Hệ thống Đào tạo & Giáo dục PDPL 2025 toàn diện được hỗ trợ bởi AI với trí tuệ văn hóa Việt Nam',
  
  features: [
    'AI-Powered Learner Analysis',
    'Personalized Learning Paths',
    'Adaptive Assessments',
    'Vietnamese Cultural Intelligence',
    'Regional Learning Adaptations',
    'Business Role Customization',
    'Real-time Progress Tracking',
    'Comprehensive Certification System',
    'Multi-language Support (Vietnamese/English)',
    'Mobile-Optimized Interface'
  ],
  
  featuresVi: [
    'Phân tích Học viên được hỗ trợ bởi AI',
    'Lộ trình Học tập Cá nhân hóa',
    'Đánh giá Thích ứng',
    'Trí tuệ Văn hóa Việt Nam',
    'Điều chỉnh Học tập theo Khu vực',
    'Tùy chỉnh theo Vai trò Kinh doanh',
    'Theo dõi Tiến độ Thời gian thực',
    'Hệ thống Chứng nhận Toàn diện',
    'Hỗ trợ Đa ngôn ngữ (Tiếng Việt/Tiếng Anh)',
    'Giao diện Tối ưu cho Di động'
  ],
  
  supportedTrainingPrograms: [
    'pdpl-2025-fundamentals',
    'data-protection-management',
    'privacy-policy-implementation',
    'security-incident-response',
    'data-subject-rights-management',
    'cross-border-data-transfer',
    'dpo-certification',
    'employee-privacy-awareness',
    'vendor-privacy-management',
    'compliance-audit-preparation'
  ],
  
  vietnameseCulturalAdaptations: {
    regions: ['north', 'central', 'south'],
    businessRoles: ['executive', 'manager', 'staff', 'dpo', 'it-admin', 'legal-counsel'],
    learningStyles: ['visual', 'auditory', 'kinesthetic', 'reading', 'mixed'],
    communicationStyles: ['formal', 'consultative', 'collaborative', 'direct'],
    culturalColorPalette: {
      sageGreen: '#6b8e6b',
      oceanBlue: '#7fa3c3',
      warmCoral: '#c17a7a',
      bambooBeige: '#f5f5dc',
      lotusWhite: '#fffef7'
    }
  },
  
  aiCapabilities: [
    'Comprehensive Learner Profiling',
    'Adaptive Content Personalization',
    'Cultural Context Analysis',
    'Learning Pattern Recognition',
    'Performance Prediction',
    'Engagement Optimization',
    'Knowledge Retention Assessment',
    'Certification Readiness Evaluation'
  ],
  
  integrationPoints: {
    veriPortalSystems: [
      'VeriCulturalOnboarding',
      'VeriComplianceWizards',
      'VeriDocumentGeneration'
    ],
    externalSystems: [
      'Learning Management Systems (LMS)',
      'Human Resource Information Systems (HRIS)',
      'Compliance Management Platforms',
      'Assessment Tools',
      'Certification Bodies'
    ]
  },
  
  usage: {
    basicUsage: `
      import { VeriTrainingIntegrationSystem } from '@verisyntra/training-integration';
      
      const MyTrainingApp = () => (
        <VeriTrainingIntegrationSystem
          veriLearnerProfile={learnerProfile}
          veriLanguage="vietnamese"
          veriSelectedPrograms={['pdpl-2025-fundamentals']}
          veriOnComplete={(result) => console.log('Training completed:', result)}
          veriOnProgressUpdate={(progress) => console.log('Progress:', progress)}
        />
      );
    `,
    
    advancedUsage: `
      import { 
        VeriTrainingIntegrationSystem, 
        veriTrainingAIEngine 
      } from '@verisyntra/training-integration';
      
      const AdvancedTrainingApp = () => {
        const [learnerProfile, setLearnerProfile] = useState(null);
        
        useEffect(() => {
          // AI-powered learner analysis
          veriTrainingAIEngine.veriAnalyzeLearner(initialProfile)
            .then(setLearnerProfile);
        }, []);
        
        return (
          <VeriTrainingIntegrationSystem
            veriLearnerProfile={learnerProfile}
            veriLanguage="vietnamese"
            veriCulturalStyle="traditional"
            veriSelectedPrograms={[
              'pdpl-2025-fundamentals',
              'dpo-certification'
            ]}
            veriOnComplete={handleTrainingCompletion}
            veriOnProgressUpdate={handleProgressUpdate}
          />
        );
      };
    `
  },
  
  technicalSpecifications: {
    framework: 'React 18+ with TypeScript 5',
    dependencies: [
      'react',
      'typescript',
      '@types/react'
    ],
    browserSupport: [
      'Chrome 90+',
      'Firefox 88+',
      'Safari 14+',
      'Edge 90+'
    ],
    mobileSupport: [
      'iOS Safari 14+',
      'Android Chrome 90+'
    ],
    accessibility: 'WCAG 2.1 AA compliant',
    performance: 'Core Web Vitals optimized',
    i18n: 'Vietnamese and English localization'
  },
  
  developmentInfo: {
    author: 'VeriSyntra Development Team',
    license: 'Proprietary - VeriSyntra PDPL 2025 Platform',
    repository: 'https://github.com/verisyntra/training-integration',
    documentation: 'https://docs.verisyntra.com/training-integration',
    support: 'support@verisyntra.com',
    lastUpdated: new Date().toISOString(),
    buildVersion: '1.0.0-2025.01'
  }
};

// Vietnamese Training Integration System Utilities
export const VeriTrainingUtils = {
  // Format Vietnamese currency
  formatVietnameseCurrency: (amount: number): string => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  },
  
  // Format Vietnamese date
  formatVietnameseDate: (date: Date): string => {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  },
  
  // Get regional greeting
  getVietnameseGreeting: (region: 'north' | 'central' | 'south', timeOfDay: 'morning' | 'afternoon' | 'evening'): string => {
    const greetings = {
      north: {
        morning: 'Chào buổi sáng',
        afternoon: 'Chào buổi chiều',
        evening: 'Chào buổi tối'
      },
      central: {
        morning: 'Xin chào buổi sáng',
        afternoon: 'Xin chào buổi chiều', 
        evening: 'Xin chào buổi tối'
      },
      south: {
        morning: 'Chào buổi sáng',
        afternoon: 'Chào buổi chiều',
        evening: 'Chào buổi tối'
      }
    };
    
    return greetings[region][timeOfDay];
  },
  
  // Calculate Vietnamese working days
  calculateVietnameseWorkingDays: (startDate: Date, endDate: Date): number => {
    let workingDays = 0;
    const currentDate = new Date(startDate);
    
    while (currentDate <= endDate) {
      const dayOfWeek = currentDate.getDay();
      // Monday = 1, Friday = 5 (Vietnamese working days)
      if (dayOfWeek >= 1 && dayOfWeek <= 5) {
        workingDays++;
      }
      currentDate.setDate(currentDate.getDate() + 1);
    }
    
    return workingDays;
  },
  
  // Generate Vietnamese certificate number
  generateVietnameseCertificateNumber: (region: string, year: number, sequence: number): string => {
    const regionCodes = {
      north: 'VN-N',
      central: 'VN-C',
      south: 'VN-S'
    };
    
    const regionCode = regionCodes[region as keyof typeof regionCodes] || 'VN-G';
    return `${regionCode}-${year}-${sequence.toString().padStart(6, '0')}`;
  },
  
  // Vietnamese phone number validation
  validateVietnamesePhoneNumber: (phone: string): boolean => {
    const vietnamesePhoneRegex = /^(\+84|84|0)(3|5|7|8|9)([0-9]{8})$/;
    return vietnamesePhoneRegex.test(phone.replace(/\s+/g, ''));
  },
  
  // Vietnamese business registration validation
  validateVietnameseBusinessRegistration: (registration: string): boolean => {
    // Simplified validation for Vietnamese business registration number
    const businessRegex = /^[0-9]{10,13}$/;
    return businessRegex.test(registration);
  }
};

// Vietnamese Training Integration Constants
export const VeriTrainingConstants = {
  SYSTEM_NAME: 'VeriSyntra Training Integration',
  VERSION: '1.0.0',
  
  // Vietnamese Language Codes
  LANGUAGES: {
    VIETNAMESE: 'vi-VN',
    ENGLISH: 'en-US'
  } as const,
  
  // Vietnamese Regional Codes
  REGIONS: {
    NORTH: 'north',
    CENTRAL: 'central', 
    SOUTH: 'south'
  } as const,
  
  // Training Program Types
  TRAINING_PROGRAMS: {
    PDPL_FUNDAMENTALS: 'pdpl-2025-fundamentals',
    DATA_PROTECTION: 'data-protection-management',
    PRIVACY_POLICY: 'privacy-policy-implementation',
    INCIDENT_RESPONSE: 'security-incident-response',
    SUBJECT_RIGHTS: 'data-subject-rights-management',
    CROSS_BORDER: 'cross-border-data-transfer',
    DPO_CERTIFICATION: 'dpo-certification',
    EMPLOYEE_AWARENESS: 'employee-privacy-awareness',
    VENDOR_MANAGEMENT: 'vendor-privacy-management',
    AUDIT_PREPARATION: 'compliance-audit-preparation'
  } as const,
  
  // Assessment Types
  ASSESSMENT_TYPES: {
    KNOWLEDGE_CHECK: 'knowledge-check',
    MODULE_ASSESSMENT: 'module-assessment',
    COMPREHENSIVE_EXAM: 'comprehensive-exam',
    PRACTICAL_APPLICATION: 'practical-application',
    SCENARIO_BASED: 'scenario-based',
    CERTIFICATION_EXAM: 'certification-exam'
  } as const,
  
  // Certification Levels
  CERTIFICATION_LEVELS: {
    BASIC: 'basic',
    PROFESSIONAL: 'professional',
    EXPERT: 'expert'
  } as const,
  
  // Learning Styles
  LEARNING_STYLES: {
    VISUAL: 'visual',
    AUDITORY: 'auditory',
    KINESTHETIC: 'kinesthetic',
    READING: 'reading',
    MIXED: 'mixed'
  } as const,
  
  // Business Roles
  BUSINESS_ROLES: {
    EXECUTIVE: 'executive',
    MANAGER: 'manager',
    STAFF: 'staff',
    DPO: 'dpo',
    IT_ADMIN: 'it-admin',
    LEGAL_COUNSEL: 'legal-counsel'
  } as const,
  
  // Cultural Communication Styles
  COMMUNICATION_STYLES: {
    FORMAL: 'formal',
    CONSULTATIVE: 'consultative',
    COLLABORATIVE: 'collaborative',
    DIRECT: 'direct'
  } as const,
  
  // Progress Tracking Events
  PROGRESS_EVENTS: {
    MODULE_START: 'module-start',
    MODULE_PROGRESS: 'module-progress',
    MODULE_COMPLETE: 'module-complete',
    ASSESSMENT_START: 'assessment-start',
    ASSESSMENT_COMPLETE: 'assessment-complete',
    MILESTONE_REACHED: 'milestone-reached',
    CERTIFICATION_EARNED: 'certification-earned'
  } as const,
  
  // Default Configuration Values
  DEFAULTS: {
    SESSION_DURATION: 45, // minutes
    WEEKLY_HOURS: 4,
    PASSING_SCORE: 80, // percentage
    MAX_ATTEMPTS: 3,
    CERTIFICATE_VALIDITY: 730, // days (2 years)
    PERSONALIZATION_THRESHOLD: 75 // percentage
  } as const
};

// Export everything for comprehensive Vietnamese Training Integration System
import VeriTrainingIntegrationSystemComponent from './components/VeriTrainingIntegrationSystem';
import { veriTrainingAIEngine as aiEngine } from './services/veriTrainingAIService';

export default {
  VeriTrainingIntegrationSystem: VeriTrainingIntegrationSystemComponent,
  VeriTrainingIntegrationInfo,
  VeriTrainingUtils,
  VeriTrainingConstants,
  veriTrainingAIEngine: aiEngine
};