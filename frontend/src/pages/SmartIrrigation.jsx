import React, { useState, useEffect } from 'react';
import { 
  Droplets, Clock, AlertTriangle, CheckCircle2, 
  Sparkles, RefreshCw, Calendar, Gauge, ShieldAlert 
} from 'lucide-react';
import api from '../services/api';

export default function SmartIrrigation({ t, lang }) {
  const [soilMoisture, setSoilMoisture] = useState(42.0);
  const [cropStage, setCropStage] = useState('Flowering & Fruit Development');
  const [soilType, setSoilType] = useState('Loamy');
  const [temperature, setTemperature] = useState(30.0);
  const [humidity, setHumidity] = useState(62.0);
  const [rainDetected, setRainDetected] = useState(false);
  const [rainProb, setRainProb] = useState(15);
  
  const [loading, setLoading] = useState(false);
  const [advice, setAdvice] = useState(null);
  const [history, setHistory] = useState([]);

  // Load live sensor values on mount
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [iotRes, histRes] = await Promise.all([
          api.getLatestIoT(),
          api.getIrrigationHistory()
        ]);
        if (iotRes.data?.latest) {
          setSoilMoisture(iotRes.data.latest.soil_moisture);
          setTemperature(iotRes.data.latest.temperature);
          setHumidity(iotRes.data.latest.humidity);
          setRainDetected(iotRes.data.latest.rain_detected);
        }
        setHistory(histRes.data);
      } catch (e) {
        console.error('Error loading initial irrigation data:', e);
      }
    };
    loadInitialData();
  }, []);

  const handleCalculate = async (e) => {
    if (e) e.preventDefault();
    try {
      setLoading(true);
      const payload = {
        crop: "Chilli (Capsicum annuum)",
        crop_growth_stage: cropStage,
        soil_moisture: parseFloat(soilMoisture),
        soil_type: soilType,
        temperature: parseFloat(temperature),
        humidity: parseFloat(humidity),
        rain_detected: rainDetected,
        rain_probability_next_24h: parseInt(rainProb)
      };
      const res = await api.calculateIrrigation(payload);
      setAdvice(res.data);
      
      // Refresh history
      const histRes = await api.getIrrigationHistory();
      setHistory(histRes.data);
    } catch (err) {
      console.error('Error calculating irrigation:', err);
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyBadge = (urgency) => {
    if (urgency === 'Immediate') return 'badge-severe';
    if (urgency === 'Scheduled') return 'badge-moderate';
    if (urgency === 'Excess Moisture Warning') return 'badge-mild';
    return 'badge-healthy';
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
          {t.irrigation.title}
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          {t.irrigation.subtitle}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        
        {/* Input Parameters Form (5 cols) */}
        <div className="lg:col-span-5">
          <form onSubmit={handleCalculate} className="agri-card p-6 space-y-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">
              Field Water & Weather Parameters
            </h2>

            {/* Soil Moisture Slider */}
            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1.5">
                <span>{t.irrigation.currentMoisture}</span>
                <span className="text-sm font-black text-emerald-400">{soilMoisture}%</span>
              </div>
              <input
                type="range"
                min="10"
                max="90"
                step="0.5"
                value={soilMoisture}
                onChange={(e) => setSoilMoisture(e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>Critical Dry (10%)</span>
                <span>Optimal (45-60%)</span>
                <span>Waterlogged (90%)</span>
              </div>
            </div>

            {/* Growth Stage */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                {t.irrigation.growthStage}
              </label>
              <select
                value={cropStage}
                onChange={(e) => setCropStage(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3.5 py-2.5 text-xs text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="Vegetative / Seedling">Vegetative / Seedling Stage</option>
                <option value="Flowering & Fruit Development">Flowering & Fruit Development (Critical Water Need)</option>
                <option value="Fruit Ripening & Harvesting">Fruit Ripening & Harvesting</option>
              </select>
            </div>

            {/* Soil Type */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Soil Texture
              </label>
              <select
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3.5 py-2.5 text-xs text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="Loamy">Loamy / Sandy Loam (High Drainage)</option>
                <option value="Black Cotton / Loamy">Black Cotton Soil (High Moisture Retention)</option>
                <option value="Clay">Clay Loam (Moderate Drainage)</option>
              </select>
            </div>

            {/* Microclimate Grid */}
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Temperature (°C)</label>
                <input
                  type="number"
                  step="0.5"
                  value={temperature}
                  onChange={(e) => setTemperature(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1">Rain Prob (24h %)</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={rainProb}
                  onChange={(e) => setRainProb(e.target.value)}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950/80 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            {/* Rain Toggle */}
            <div className="flex items-center justify-between rounded-xl bg-slate-950/60 p-3 border border-slate-800">
              <span className="text-xs font-semibold text-slate-300">Live Rain Detected</span>
              <input
                type="checkbox"
                checked={rainDetected}
                onChange={(e) => setRainDetected(e.target.checked)}
                className="h-4 w-4 rounded accent-emerald-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-xs font-bold text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-950/30"
            >
              <Droplets className="h-4 w-4" />
              <span>{loading ? t.common.loading : t.irrigation.calcButton}</span>
            </button>
          </form>
        </div>

        {/* Advisory Output (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {advice ? (
            <div className="agri-card p-6 border-emerald-500/40 space-y-5">
              
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                    {t.irrigation.advisoryTitle}
                  </span>
                  <div className="flex items-center gap-2.5 mt-1">
                    <span className={`text-sm font-extrabold px-3 py-1 rounded-lg ${getUrgencyBadge(advice.urgency_level)}`}>
                      {advice.urgency_level}
                    </span>
                    <span className="text-xs text-slate-400">
                      {advice.irrigation_required ? '• Irrigation Recommended' : '• Postpone Water Application'}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs text-slate-400 block font-semibold">{t.irrigation.waterRequired}</span>
                  <span className="text-2xl font-black text-white">
                    {advice.water_requirement_liters_per_acre.toLocaleString()} <span className="text-xs font-medium text-slate-400">L/acre</span>
                  </span>
                </div>
              </div>

              {/* Timing & Drip Duration Grid */}
              <div className="grid grid-cols-2 gap-3 py-2 border-b border-slate-800">
                <div className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                  <span className="text-xs font-semibold text-slate-400 block mb-1 flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-emerald-400" />
                    {t.irrigation.timing}
                  </span>
                  <p className="text-xs sm:text-sm font-bold text-white">
                    {advice.recommended_timing}
                  </p>
                </div>

                <div className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                  <span className="text-xs font-semibold text-slate-400 block mb-1 flex items-center gap-1">
                    <Gauge className="h-3.5 w-3.5 text-blue-400" />
                    {t.irrigation.dripDuration}
                  </span>
                  <p className="text-xs sm:text-sm font-bold text-white">
                    {advice.recommended_duration_minutes} {t.irrigation.minutes} (16mm inline drip)
                  </p>
                </div>
              </div>

              {/* Rationale */}
              <div className="py-2 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                  {t.irrigation.reason}
                </h3>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
                  {lang === 'mr' ? advice.reason_mr : advice.reason_en}
                </p>
              </div>

              {/* Action items */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
                  <Sparkles className="h-4 w-4" />
                  <span>{t.irrigation.actionItems}</span>
                </h3>
                <ul className="space-y-2">
                  {(lang === 'mr' ? advice.action_items_mr : advice.action_items_en).map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-slate-300">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>
          ) : (
            <div className="agri-card p-12 text-center flex flex-col items-center justify-center">
              <Droplets className="h-12 w-12 text-blue-400 mb-3 animate-pulse" />
              <p className="text-sm font-bold text-white">
                Calculate Precision Irrigation
              </p>
              <p className="text-xs text-slate-400 max-w-sm mt-1">
                Adjust the field parameters or keep live IoT readings, then click calculate to formulate an optimal water scheduling plan.
              </p>
            </div>
          )}

          {/* Recent Recommendations Log */}
          {history.length > 0 && (
            <div className="agri-card p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                Recent Irrigation Logs
              </h3>
              <div className="divide-y divide-slate-800">
                {history.slice(0, 4).map((h) => (
                  <div key={h.id} className="py-2.5 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-bold text-white">{h.timing}</span>
                      <span className="text-slate-400 block text-[11px]">Moisture: {h.soil_moisture}%</span>
                    </div>
                    <span className={`px-2 py-0.5 rounded-md font-semibold ${getUrgencyBadge(h.water_level)}`}>
                      {h.water_level}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
