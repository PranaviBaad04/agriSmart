import React, { useState } from 'react';
import { 
  FlaskConical, Sparkles, CheckCircle2, AlertTriangle, 
  HelpCircle, RefreshCw, Layers, ShieldCheck, ArrowRight 
} from 'lucide-react';
import api from '../services/api';

export default function SoilHealth({ t, lang }) {
  const [sampleName, setSampleName] = useState('Main Chilli Plot A');
  const [ph, setPh] = useState(6.4);
  const [nitrogen, setNitrogen] = useState(120);
  const [phosphorus, setPhosphorus] = useState(45);
  const [potassium, setPotassium] = useState(80);
  const [organicCarbon, setOrganicCarbon] = useState(0.65);
  const [soilType, setSoilType] = useState('Sandy Loam / Loamy');
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    try {
      setLoading(true);
      const res = await api.analyzeSoil({
        sample_name: sampleName,
        ph: parseFloat(ph),
        nitrogen: parseFloat(nitrogen),
        phosphorus: parseFloat(phosphorus),
        potassium: parseFloat(potassium),
        organic_carbon: parseFloat(organicCarbon),
        soil_type: soilType
      });
      setResult(res.data);
    } catch (err) {
      console.error('Soil analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const setPreset = (preset) => {
    if (preset === 'ideal') {
      setPh(6.5); setNitrogen(130); setPhosphorus(48); setPotassium(85); setOrganicCarbon(0.85);
    } else if (preset === 'acidic') {
      setPh(5.2); setNitrogen(80); setPhosphorus(22); setPotassium(55); setOrganicCarbon(0.4);
    } else if (preset === 'alkaline') {
      setPh(8.4); setNitrogen(115); setPhosphorus(68); setPotassium(95); setOrganicCarbon(0.5);
    }
  };

  const getStatusBadge = (status) => {
    const s = (status || '').toLowerCase();
    if (s.includes('deficient')) return 'badge-severe';
    if (s.includes('low') || s.includes('high')) return 'badge-moderate';
    return 'badge-healthy';
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
          {t.soil.title}
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          {t.soil.subtitle}
        </p>
      </div>

      {/* Preset Buttons */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-slate-400">Quick Test Presets:</span>
        <button
          onClick={() => setPreset('ideal')}
          className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-1 text-xs font-medium text-emerald-400 hover:bg-slate-800"
        >
          Fertile Loam (Optimal)
        </button>
        <button
          onClick={() => setPreset('acidic')}
          className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-1 text-xs font-medium text-amber-400 hover:bg-slate-800"
        >
          Acidic Low-N Soil
        </button>
        <button
          onClick={() => setPreset('alkaline')}
          className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-1 text-xs font-medium text-purple-400 hover:bg-slate-800"
        >
          Alkaline Calcareous Soil
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        
        {/* Soil Testing Form (5 cols) */}
        <div className="lg:col-span-5">
          <form onSubmit={handleAnalyze} className="agri-card p-6 space-y-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">
              Soil Test Report Values
            </h2>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.soil.sampleName}
              </label>
              <input
                type="text"
                value={sampleName}
                onChange={(e) => setSampleName(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>

            {/* pH */}
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1">
                <span>{t.soil.phInput}</span>
                <span className="text-emerald-400 font-bold">{ph}</span>
              </div>
              <input
                type="number"
                step="0.1"
                min="3.0"
                max="10.0"
                value={ph}
                onChange={(e) => setPh(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>

            {/* NPK Grid */}
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Nitrogen (N)</label>
                <input
                  type="number"
                  value={nitrogen}
                  onChange={(e) => setNitrogen(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-2.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Phosphorus (P)</label>
                <input
                  type="number"
                  value={phosphorus}
                  onChange={(e) => setPhosphorus(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-2.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Potassium (K)</label>
                <input
                  type="number"
                  value={potassium}
                  onChange={(e) => setPotassium(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-2.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            {/* Organic Carbon */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.soil.ocInput}
              </label>
              <input
                type="number"
                step="0.05"
                min="0.1"
                max="3.0"
                value={organicCarbon}
                onChange={(e) => setOrganicCarbon(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3.5 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-xs font-bold text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-950/30"
            >
              <FlaskConical className="h-4 w-4" />
              <span>{loading ? t.common.loading : t.soil.analyzeButton}</span>
            </button>
          </form>
        </div>

        {/* Diagnostic Output (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {result ? (
            <div className="agri-card p-6 border-emerald-500/40 space-y-5">
              
              {/* Overall Health Score Card */}
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                    Soil Health Assessment
                  </span>
                  <h3 className="text-xl font-extrabold text-white mt-0.5">
                    {result.sample_name}
                  </h3>
                  <span className="text-xs font-semibold text-slate-400 mt-1 block">
                    {result.overall_status}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-[11px] text-slate-400 block font-semibold">{t.soil.healthScore}</span>
                    <span className="text-3xl font-black text-emerald-400">
                      {result.overall_health_score}<span className="text-sm font-normal text-slate-500">/100</span>
                    </span>
                  </div>
                </div>
              </div>

              {/* 5 Nutrients Grid Breakdown */}
              <div className="space-y-3">
                {[
                  result.ph_rating,
                  result.nitrogen_rating,
                  result.phosphorus_rating,
                  result.potassium_rating,
                  result.organic_carbon_rating
                ].map((nutr, idx) => (
                  <div key={idx} className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white">
                        {nutr.unit === 'pH' ? 'Soil Reaction (pH)' : `${nutr.unit} Level: ${nutr.value} ${nutr.unit}`}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${getStatusBadge(nutr.status)}`}>
                        {nutr.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">
                      {lang === 'mr' ? nutr.advice_mr : nutr.advice_en}
                    </p>
                    <span className="text-[10px] text-slate-500 mt-1 block">
                      Target Range: {nutr.optimal_range}
                    </span>
                  </div>
                ))}
              </div>

              {/* Fertilizer Schedule */}
              <div className="pt-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2.5 flex items-center gap-1.5">
                  <Sparkles className="h-4 w-4" />
                  <span>{t.soil.fertilizerSchedule}</span>
                </h3>
                <ul className="space-y-2">
                  {(lang === 'mr' ? result.fertilizer_recommendations_mr : result.fertilizer_recommendations_en).map((rec, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>
          ) : (
            <div className="agri-card p-12 text-center flex flex-col items-center justify-center">
              <FlaskConical className="h-12 w-12 text-amber-400 mb-3 animate-pulse" />
              <p className="text-sm font-bold text-white">
                Run Soil Health Analysis
              </p>
              <p className="text-xs text-slate-400 max-w-sm mt-1">
                Enter your soil laboratory test values or select a preset to generate tailored NPK balancing and pH correction schedules.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
