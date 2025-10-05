import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing';
import VeriSyntraApp from './verisyntra/VeriSyntraApp';
import VeriCulturalOnboardingSystem from './components/VeriPortal/CulturalOnboarding/VeriCulturalOnboardingSystem';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/app" element={<VeriSyntraApp />} />
        <Route path="/veriportal" element={<VeriCulturalOnboardingSystem />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;