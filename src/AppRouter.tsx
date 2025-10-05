import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing';
import VeriSyntraApp from './verisyntra/VeriSyntraApp.tsx';
import { VeriComplianceWizardSystem, VeriDocumentGenerationSystem, VeriBusinessIntelligenceSystem, VeriCulturalOnboardingSystem } from './components/VeriPortal';
import VeriSystemIntegrationSystem from './components/VeriPortal/SystemIntegration/components/VeriSystemIntegrationSystem';

// Default Vietnamese Business Context for Demo
const defaultVeriBusinessContext = {
  veriBusinessId: 'demo-business-001',
  veriBusinessName: 'VeriSyntra Demo Enterprise',
  veriBusinessNameVi: 'VeriSyntra Doanh Nghiệp Demo',
  veriIndustryType: 'technology',
  veriBusinessSize: 'medium' as const,
  veriRegionalLocation: 'north' as const,
  veriCulturalPreferences: {
    veriCommunicationStyle: 'collaborative' as const,
    veriDecisionMakingStyle: 'data-driven' as const,
    veriReportingPreferences: 'visual' as const,
    veriVisualizationStyle: 'modern' as const,
    veriDataPresentationFormat: 'mixed' as const
  },
  veriComplianceLevel: 'advanced' as const,
  veriMarketSegment: 'enterprise-technology',
  veriBusinessObjectives: [
    'Tuân thủ PDPL 2025',
    'Tối ưu hóa hiệu suất kinh doanh',
    'Nâng cao trải nghiệm khách hàng',
    'Mở rộng thị trường'
  ]
};

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/app" element={<VeriSyntraApp />} />
        <Route path="/veriportal" element={<VeriComplianceWizardSystem />} />
        <Route path="/veriportal/cultural-onboarding" element={<VeriCulturalOnboardingSystem />} />
        <Route path="/veriportal/documents" element={<VeriDocumentGenerationSystem />} />
        <Route path="/veriportal/business-intelligence" element={<VeriBusinessIntelligenceSystem veriBusinessContext={defaultVeriBusinessContext} veriLanguage="vietnamese" />} />
        <Route path="/veriportal/system-integration" element={<VeriSystemIntegrationSystem />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;