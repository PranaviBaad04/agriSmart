import React from 'react';
import { 
  Sprout, Globe, Activity, Cloud, Wifi, Cpu, Menu, X 
} from 'lucide-react';

export default function Navbar({ 
  lang, 
  setLang, 
  t, 
  isDemoMode, 
  toggleDemoMode, 
  mobileMenuOpen, 
  setMobileMenuOpen 
}) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Left: Mobile Toggle & Brand */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>

          <div className="flex items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 shadow-lg shadow-emerald-500/20">
              <Sprout className="h-6 w-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-tight text-white flex items-center gap-1.5">
                Agri<span className="text-emerald-400">Smart</span>
              </span>
              <span className="hidden text-xs text-slate-400 sm:inline-block">
                {t.tagline}
              </span>
            </div>
          </div>
        </div>

        {/* Right: Badges, Demo Switcher, Language Toggle */}
        <div className="flex items-center gap-2.5 sm:gap-4">
          
          {/* Cloudinary CDN Indicator */}
          <div className="hidden items-center gap-1.5 rounded-full border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs font-medium text-sky-400 md:flex">
            <Cloud className="h-3.5 w-3.5" />
            <span>Cloudinary CDN</span>
          </div>

          {/* IoT Mode Badge / Switch */}
          <button
            onClick={toggleDemoMode}
            title="Click to toggle Demo simulation / Live ESP32 mode"
            className={`flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium transition-all ${
              isDemoMode 
                ? 'border-amber-500/30 bg-amber-500/10 text-amber-300 hover:bg-amber-500/20' 
                : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20'
            }`}
          >
            <span className="relative flex h-2 w-2">
              <span className={`absolute inline-flex h-full w-full animate-ping rounded-full opacity-75 ${
                isDemoMode ? 'bg-amber-400' : 'bg-emerald-400'
              }`}></span>
              <span className={`relative inline-flex h-2 w-2 rounded-full ${
                isDemoMode ? 'bg-amber-500' : 'bg-emerald-500'
              }`}></span>
            </span>
            <Cpu className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">
              {isDemoMode ? t.common.demoMode : t.common.liveMode}
            </span>
          </button>

          {/* Language Switcher */}
          <div className="flex items-center rounded-xl border border-slate-800 bg-slate-900/90 p-0.5 shadow-inner">
            <button
              onClick={() => setLang('en')}
              className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-all ${
                lang === 'en'
                  ? 'bg-emerald-500 text-white shadow'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => setLang('mr')}
              className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-all font-['Noto_Sans_Devanagari'] ${
                lang === 'mr'
                  ? 'bg-emerald-500 text-white shadow'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              मराठी
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
