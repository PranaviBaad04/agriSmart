import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  ScanEye,
  History,
  Activity,
  Droplets,
  FlaskConical,
  Wheat,
  CloudSun,
  BotMessageSquare
} from 'lucide-react';

export default function Sidebar({ t, mobileMenuOpen, setMobileMenuOpen }) {
  const navItems = [
    { path: '/', label: t.nav.dashboard, icon: LayoutDashboard },
    { path: '/disease', label: t.nav.diseaseDetection, icon: ScanEye, badge: 'AI' },
    { path: '/history', label: t.nav.diseaseHistory, icon: History },
    { path: '/iot', label: t.nav.iotMonitoring, icon: Activity, badge: 'IoT' },
    { path: '/irrigation', label: t.nav.smartIrrigation, icon: Droplets },
    { path: '/soil', label: t.nav.soilHealth, icon: FlaskConical },
    { path: '/crop', label: t.nav.cropRecommendation, icon: Wheat },
    { path: '/weather', label: t.nav.weather, icon: CloudSun },
    { path: '/chat', label: t.nav.aiAssistant, icon: BotMessageSquare, badge: 'AI' },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 transform border-r border-slate-800 bg-slate-950/95 backdrop-blur-xl p-4 transition-transform duration-300 ease-in-out lg:static lg:translate-x-0 ${
        mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        
        {/* Navigation List */}
        <nav className="mt-14 lg:mt-4 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `group flex items-center justify-between rounded-xl px-3.5 py-3 text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-emerald-500/20 to-teal-500/10 text-emerald-400 border border-emerald-500/30 shadow-lg shadow-emerald-950/20'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="flex items-center gap-3">
                      <Icon className={`h-5 w-5 transition-transform duration-200 group-hover:scale-110 ${
                        isActive ? 'text-emerald-400' : 'text-slate-400'
                      }`} />
                      <span>{item.label}</span>
                    </div>

                    {item.badge && (
                      <span className={`rounded-md px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
                        isActive 
                          ? 'bg-emerald-500/30 text-emerald-300' 
                          : 'bg-slate-800 text-slate-400'
                      }`}>
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Bottom System Info Widget */}
        <div className="absolute bottom-4 left-4 right-4 rounded-xl border border-slate-800/80 bg-slate-900/60 p-3.5">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
            <span>Primary Crop:</span>
            <span className="font-semibold text-emerald-400">Chilli G-4</span>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ML Model:</span>
            <span className="font-semibold text-slate-300">MobileNetV2</span>
          </div>
        </div>

      </aside>
    </>
  );
}
