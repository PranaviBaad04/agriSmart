import React, { useState } from 'react';
import { 
  Wheat, Sparkles, CheckCircle2, Droplets, 
  Calendar, Layers, TrendingUp, Info 
} from 'lucide-react';
import api from '../services/api';

export default function CropRecommendation({ t, lang }) {
  const [season, setSeason] = useState('Kharif');
  const [region, setRegion] = useState('Maharashtra (Western Ghats & Deccan Plateau)');
  const [soilType, setSoilType] = useState('Black Cotton / Loamy');
  const [ph, setPh] = useState(6.5);
  const [nitrogen, setNitrogen] = useState(125);
  const [phosphorus, setPhosphorus] = useState(48);
  const [potassium, setPotassium] = useState(85);
  const [rainfall, setRainfall] = useState(850);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRecommend = async (e) => {
    if (e) e.preventDefault();
    try {
      setLoading(true);
      const res = await api.recommendCrops({
        season,
        region,
        soil_type: soilType,
        ph: parseFloat(ph),
        nitrogen: parseFloat(nitrogen),
        phosphorus: parseFloat(phosphorus),
        potassium: parseFloat(potassium),
        rainfall_annual_mm: parseFloat(rainfall)
      });
      setResult(res.data);
    } catch (err) {
      console.error('Crop recommendation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
          {t.crop.title}
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          {t.crop.subtitle}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        
        {/* Form Column (4 cols) */}
        <div className="lg:col-span-4">
          <form onSubmit={handleRecommend} className="agri-card p-5 space-y-3.5">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Field & Climate Profiling
            </h2>

            {/* Season */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.crop.season}
              </label>
              <select
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="Kharif">Kharif (Monsoon: June - Oct)</option>
                <option value="Rabi">Rabi (Winter: Nov - March)</option>
                <option value="Zaid / Summer">Zaid (Summer: March - June)</option>
              </select>
            </div>

            {/* Region */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.crop.region}
              </label>
              <select
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="Western Maharashtra">Western Maharashtra / Pune / Satara</option>
                <option value="Vidarbha / Marathwada">Vidarbha / Marathwada / Khandesh</option>
                <option value="Southern India">Southern Plateau / Andhra / Karnataka</option>
              </select>
            </div>

            {/* Soil Type */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t.crop.soilType}
              </label>
              <select
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="Black Cotton / Loamy">Black Cotton Soil (Regur)</option>
                <option value="Sandy Loam / Loamy">Sandy Loam / Alluvial Loam</option>
                <option value="Red Loamy">Red Loamy Soil</option>
              </select>
            </div>

            {/* pH & Rainfall */}
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Soil pH</label>
                <input
                  type="number"
                  step="0.1"
                  value={ph}
                  onChange={(e) => setPh(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-2.5 py-1.5 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[11px] text-slate-400 mb-1">Rainfall (mm)</label>
                <input
                  type="number"
                  value={rainfall}
                  onChange={(e) => setRainfall(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-2.5 py-1.5 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-xs font-bold text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-950/30"
            >
              <Wheat className="h-4 w-4" />
              <span>{loading ? t.common.loading : t.crop.recommendButton}</span>
            </button>
          </form>
        </div>

        {/* Results Column (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          
          {result ? (
            <div className="space-y-4">
              
              <div className="agri-card p-4 border-emerald-500/40 flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                    Primary Agronomic Match
                  </span>
                  <h3 className="text-lg font-black text-white mt-0.5">
                    {result.primary_recommendation}
                  </h3>
                  <p className="text-xs text-slate-300 mt-1">
                    {result.soil_suitability_summary}
                  </p>
                </div>
              </div>

              {/* Crop Cards */}
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {result.recommended_crops.map((crop, idx) => (
                  <div
                    key={idx}
                    className={`agri-card p-4 transition-all ${
                      idx === 0 ? 'border-emerald-500/50 bg-emerald-950/20' : 'border-slate-800'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-base font-black text-white">
                          {lang === 'mr' ? crop.marathi_name : crop.crop_name}
                        </h4>
                        <span className="text-[11px] text-slate-400 block mt-0.5">
                          {crop.category}
                        </span>
                      </div>

                      <div className="text-right">
                        <span className={`text-xs font-black px-2.5 py-1 rounded-md ${
                          crop.suitability_score >= 85 ? 'badge-healthy' : 'badge-moderate'
                        }`}>
                          {crop.suitability_score}% Match
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-2 mt-3 text-[11px] text-slate-300 border-t border-slate-800/80 pt-2.5">
                      <div>
                        <span className="text-slate-500 block">Duration:</span>
                        <span className="font-semibold">{crop.duration_days}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block">Ideal pH:</span>
                        <span className="font-semibold">{crop.soil_ph_ideal}</span>
                      </div>
                      <div className="col-span-2">
                        <span className="text-slate-500 block">Expected Yield:</span>
                        <span className="font-semibold text-emerald-400">{crop.expected_yield_per_acre}</span>
                      </div>
                    </div>

                    <div className="mt-3 pt-2.5 border-t border-slate-800/80">
                      <ul className="space-y-1">
                        {(lang === 'mr' ? crop.reasons_mr : crop.reasons_en).map((r, rIdx) => (
                          <li key={rIdx} className="text-[11px] text-slate-300 flex items-start gap-1.5">
                            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                            <span>{r}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                  </div>
                ))}
              </div>

            </div>
          ) : (
            <div className="agri-card p-12 text-center flex flex-col items-center justify-center">
              <Wheat className="h-12 w-12 text-emerald-400 mb-3 animate-pulse" />
              <p className="text-sm font-bold text-white">
                Find Optimal Crops for Your Field
              </p>
              <p className="text-xs text-slate-400 max-w-sm mt-1">
                Select your agricultural season and soil characteristics to evaluate commercial feasibility and expected yields.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
