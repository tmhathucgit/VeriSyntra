import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing';
import VeriSyntraApp from './verisyntra/VeriSyntraApp';
import { VeriComplianceWizardSystem } from './components/VeriPortal/ComplianceWizards';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/app" element={<VeriSyntraApp />} />
        <Route path="/veriportal" element={<VeriComplianceWizardSystem />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;