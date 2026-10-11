import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Droplets, Thermometer, Wind, CloudRain, Activity, 
  ScanEye, FlaskConical, Wheat, BotMessageSquare, ArrowUpRight,
  ShieldCheck, AlertTriangle, Clock, RefreshCw, CloudSun
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer 
} from 'recharts';
import api from '../services/api';

export default function Dashboard({ t, lang }) {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDashboardData = async () => {
    try {
      setRefreshing(true);
      const [summaryRes, historyRes] = await Promise.all([
        api.getDashboardSummary(),
        api.getIoTHistory({ hours: 24, limit: 15 })
      ]);
      setData(summaryRes.data);
      
      const formattedHistory = historyRes.data.map(item => ({
        time: new Date(/[zZ]|[+-]\d{2}:?\d{2}$/.test(item.timestamp) ? item.timestamp : item.timestamp + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        moisture: item.soil_moisture,
        temp: item.temperature,
        humidity: item.humidity,
        ph: item.ph
      }));
      setHistory(formattedHistory);
    } catch (err) {
      console.error('Error fetching dashboard summary:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 15000); // 15s refresh
    return () => clearInterval(interval);
  }, []);

  if (loading && !data) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <RefreshCw className="h-8 w-8 animate-spin text-emerald-500" />
          <p className="text-sm text-slate-400">{t.common.loading}</p>
        </div>
      </div>
    );
  }

  const telemetry = data?.telemetry?.latest || {
    soil_moisture: 44.0,
    ph: 6.4,
    temperature: 29.5,
    humidity: 68,
    nitrogen: 120,
    phosphorus: 45,
    potassium: 80,
    rain_detected: false
  };

  const weather = data?.weather || {
    temperature_c: 29.5,
    humidity_percent: 68,
    weather_condition: "Partly Cloudy",
    forecast_summary_en: "Clear sky with optimal sunshine.",
    forecast_summary_mr: "स्वच्छ आकाश आणि भरपूर सूर्यप्रकाश."
  };

  const recentScans = data?.recent_detections || [];
  const quickStatus = data?.quick_status || {};

  return (
    <div className="space-y-6">
      
      {/* Header Bar */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
            {t.dashboard.title}
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            {t.dashboard.subtitle}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchDashboardData}
            disabled={refreshing}
            className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-3.5 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition-all shadow-sm"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? 'animate-spin text-emerald-400' : ''}`} />
            <span>{refreshing ? 'Syncing...' : 'Sync Data'}</span>
          </button>
        </div>
      </div>

      {/* 4 Top Telemetry KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        
        {/* Soil Moisture */}
        <div className="agri-card p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {t.dashboard.soilMoisture}
            </span>
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
              <Droplets className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-black text-white">{telemetry.soil_moisture ?? '--'}%</span>
            <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${
              telemetry.soil_moisture >= 35 && telemetry.soil_moisture <= 65 
                ? 'bg-emerald-500/20 text-emerald-300' 
                : 'bg-amber-500/20 text-amber-300'
            }`}>
              {quickStatus.soil_moisture_status || 'Optimal'}
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-400">
            Field threshold: 35% - 65%
          </p>
        </div>

        {/* Soil pH */}
        <div className="agri-card p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {t.dashboard.soilPh}
            </span>
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
              <FlaskConical className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-black text-white">{telemetry.ph ?? '--'}</span>
            <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-emerald-500/20 text-emerald-300">
              {quickStatus.ph_status || 'Optimal'}
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-400">
            Target: 6.0 - 7.0 for Chilli
          </p>
        </div>

        {/* Field Temp & Humidity */}
        <div className="agri-card p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {t.dashboard.temperature} / {t.dashboard.humidity}
            </span>
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
              <Thermometer className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-3">
            <span className="text-3xl font-black text-white">{telemetry.temperature ?? '--'}°C</span>
            <span className="text-xl font-bold text-slate-400">{telemetry.humidity ?? '--'}% RH</span>
          </div>
          <p className="mt-2 text-xs text-slate-400">
            Ambient micro-climate sensor
          </p>
        </div>

        {/* Rain & Weather */}
        <div className="agri-card p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {t.dashboard.rainStatus}
            </span>
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
              <CloudRain className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black text-white">
              {telemetry.rain_detected ? 'Rain Active' : 'No Rain'}
            </span>
            <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${
              telemetry.rain_detected ? 'bg-blue-500/20 text-blue-300' : 'bg-slate-800 text-slate-300'
            }`}>
              {weather.weather_condition}
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-400">
            Rain sensor + 7-day forecast
          </p>
        </div>

      </div>

      {/* Quick Farm Actions */}
      <div className="agri-card p-6">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">
          {t.dashboard.quickActions}
        </h2>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          
          <Link
            to="/disease"
            className="group flex flex-col items-start rounded-xl border border-emerald-500/30 bg-gradient-to-br from-emerald-500/10 to-teal-500/5 p-4 transition-all hover:border-emerald-500 hover:bg-emerald-500/20 shadow-lg shadow-emerald-950/20"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/20 text-emerald-400 group-hover:scale-110 transition-transform">
              <ScanEye className="h-5 w-5" />
            </div>
            <span className="mt-3 text-sm font-bold text-white group-hover:text-emerald-300">
              {t.nav.diseaseDetection}
            </span>
            <span className="text-xs text-slate-400 mt-0.5">MobileNetV2 AI Model</span>
          </Link>

          <Link
            to="/irrigation"
            className="group flex flex-col items-start rounded-xl border border-blue-500/30 bg-gradient-to-br from-blue-500/10 to-cyan-500/5 p-4 transition-all hover:border-blue-500 hover:bg-blue-500/20"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/20 text-blue-400 group-hover:scale-110 transition-transform">
              <Droplets className="h-5 w-5" />
            </div>
            <span className="mt-3 text-sm font-bold text-white group-hover:text-blue-300">
              {t.nav.smartIrrigation}
            </span>
            <span className="text-xs text-slate-400 mt-0.5">Water balance advisor</span>
          </Link>

          <Link
            to="/soil"
            className="group flex flex-col items-start rounded-xl border border-amber-500/30 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-4 transition-all hover:border-amber-500 hover:bg-amber-500/20"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-500/20 text-amber-400 group-hover:scale-110 transition-transform">
              <FlaskConical className="h-5 w-5" />
            </div>
            <span className="mt-3 text-sm font-bold text-white group-hover:text-amber-300">
              {t.nav.soilHealth}
            </span>
            <span className="text-xs text-slate-400 mt-0.5">NPK & pH Diagnostics</span>
          </Link>

          <Link
            to="/chat"
            className="group flex flex-col items-start rounded-xl border border-purple-500/30 bg-gradient-to-br from-purple-500/10 to-fuchsia-500/5 p-4 transition-all hover:border-purple-500 hover:bg-purple-500/20"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-500/20 text-purple-400 group-hover:scale-110 transition-transform">
              <BotMessageSquare className="h-5 w-5" />
            </div>
            <span className="mt-3 text-sm font-bold text-white group-hover:text-purple-300">
              {t.nav.aiAssistant}
            </span>
            <span className="text-xs text-slate-400 mt-0.5">English + मराठी</span>
          </Link>

        </div>
      </div>

      {/* Main Charts & Recent Detections Section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        
        {/* Soil Moisture Chart (2 cols) */}
        <div className="agri-card p-6 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-white">
                {t.iot.moistureChart}
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Hourly telemetry from capacitive root-zone sensor
              </p>
            </div>
            <Link
              to="/iot"
              className="flex items-center gap-1 text-xs font-semibold text-emerald-400 hover:text-emerald-300"
            >
              <span>{t.nav.iotMonitoring}</span>
              <ArrowUpRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorMoisture" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#475569" fontSize={11} tickLine={false} />
                <YAxis stroke="#475569" fontSize={11} tickLine={false} domain={[20, 80]} unit="%" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#fff' }}
                  itemStyle={{ color: '#10b981' }}
                />
                <Area 
                  type="monotone" 
                  dataKey="moisture" 
                  stroke="#10b981" 
                  strokeWidth={2.5} 
                  fillOpacity={1} 
                  fill="url(#colorMoisture)" 
                  name="Moisture (%)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Disease Scans */}
        <div className="agri-card p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold text-white">
                {t.dashboard.recentDetections}
              </h2>
              <Link
                to="/history"
                className="flex items-center gap-1 text-xs font-semibold text-emerald-400 hover:text-emerald-300"
              >
                <span>{t.common.all}</span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </Link>
            </div>

            {recentScans.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <ScanEye className="h-10 w-10 text-slate-600 mb-2" />
                <p className="text-xs text-slate-400 max-w-[200px]">
                  {t.dashboard.noRecentScans}
                </p>
                <Link
                  to="/disease"
                  className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-emerald-500"
                >
                  <ScanEye className="h-3.5 w-3.5" />
                  <span>Scan Leaf</span>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {recentScans.map((scan) => {
                  const isHealthy = scan.disease === 'Healthy_Leaf';
                  return (
                    <div
                      key={scan.id}
                      className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/60 p-2.5 transition-all hover:border-slate-700"
                    >
                      <img
                        src={scan.image_url}
                        alt={scan.disease}
                        className="h-12 w-12 rounded-lg object-cover border border-slate-700"
                        onError={(e) => {
                          e.target.src = 'https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=150&auto=format&fit=crop&q=60';
                        }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-xs font-bold text-white truncate">
                            {scan.disease.replace(/_/g, ' ')}
                          </p>
                          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-md ${
                            isHealthy ? 'badge-healthy' : 'badge-moderate'
                          }`}>
                            {scan.confidence.toFixed(0)}%
                          </span>
                        </div>
                        <div className="flex items-center justify-between mt-1 text-[11px] text-slate-400">
                          <span>{scan.severity || (isHealthy ? 'Healthy' : 'Mild')}</span>
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {new Date(scan.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-slate-800">
            <Link
              to="/disease"
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 py-2.5 text-xs font-bold text-white hover:bg-emerald-500 transition-all shadow-md shadow-emerald-950/30"
            >
              <ScanEye className="h-4 w-4" />
              <span>{t.disease.detectButton}</span>
            </Link>
          </div>
        </div>

      </div>

    </div>
  );
}
