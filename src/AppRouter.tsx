import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing';
import VeriSyntraApp from './verisyntra/VeriSyntraApp';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/app" element={<VeriSyntraApp />} />
        <Route path="/verisyntra" element={<VeriSyntraApp />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;