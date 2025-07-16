import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Layout from './components/Layout';
import HomePage from './components/HomePage';
import MedMixDashboard from './components/MedMixDashboard';
import DecisionAidViewer from './components/DecisionAidViewer';
import HelpBot from './components/HelpBot';
import ClarifyWidget from './components/ClarifyWidget';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<MedMixDashboard />} />
          <Route path="/analyzer" element={<DecisionAidViewer />} />
          <Route path="/helpbot" element={<HelpBot />} />
          <Route path="/widget" element={<div className="max-w-3xl mx-auto my-12 px-4"><ClarifyWidget /></div>} />
          <Route path="*" element={<div className="p-12 text-center"><h1 className="text-3xl font-bold text-gray-800">404 - Page Not Found</h1></div>} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
