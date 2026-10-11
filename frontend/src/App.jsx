import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { translations } from './i18n/translations';
import api from './services/api';

import Navbar from './layouts/Navbar';
import Sidebar from './layouts/Sidebar';

import Dashboard from './pages/Dashboard';
import DiseaseDetection from './pages/DiseaseDetection';
import DiseaseHistory from './pages/DiseaseHistory';
import IoTMonitoring from './pages/IoTMonitoring';
import SmartIrrigation from './pages/SmartIrrigation';
import SoilHealth from './pages/SoilHealth';
import CropRecommendation from './pages/CropRecommendation';
import WeatherPage from './pages/WeatherPage';
import AIAssistant from './pages/AIAssistant';

export default function App() {
  const [lang, setLang] = useState('en');
  const [isDemoMode, setIsDemoMode] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const t = translations[lang] || translations.en;

  const toggleDemoMode = async () => {
    const nextState = !isDemoMode;
    setIsDemoMode(nextState);
    try {
      await api.toggleIoTDemo(nextState);
    } catch (e) {
      console.error('Error toggling demo mode on backend:', e);
    }
  };

  return (
    <Router>
      <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
        
        {/* Top Navigation */}
        <Navbar
          lang={lang}
          setLang={setLang}
          t={t}
          isDemoMode={isDemoMode}
          toggleDemoMode={toggleDemoMode}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
        />

        <div className="flex flex-1 overflow-hidden">
          
          {/* Side Navigation */}
          <Sidebar
            t={t}
            mobileMenuOpen={mobileMenuOpen}
            setMobileMenuOpen={setMobileMenuOpen}
          />

          {/* Main Content Area */}
          <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
            <Routes>
              <Route path="/" element={<Dashboard t={t} lang={lang} />} />
              <Route path="/disease" element={<DiseaseDetection t={t} lang={lang} />} />
              <Route path="/history" element={<DiseaseHistory t={t} lang={lang} />} />
              <Route 
                path="/iot" 
                element={
                  <IoTMonitoring 
                    t={t} 
                    lang={lang} 
                    isDemoMode={isDemoMode} 
                    toggleDemoMode={toggleDemoMode} 
                  />
                } 
              />
              <Route path="/irrigation" element={<SmartIrrigation t={t} lang={lang} />} />
              <Route path="/soil" element={<SoilHealth t={t} lang={lang} />} />
              <Route path="/crop" element={<CropRecommendation t={t} lang={lang} />} />
              <Route path="/weather" element={<WeatherPage t={t} lang={lang} />} />
              <Route path="/chat" element={<AIAssistant t={t} lang={lang} />} />
            </Routes>
          </main>

        </div>
      </div>
    </Router>
  );
}
