import React, { useState, useEffect } from 'react';
import { 
  History, Search, Filter, Trash2, ExternalLink, 
  Calendar, Eye, RefreshCw, X, ShieldAlert, Sparkles, CheckCircle2 
} from 'lucide-react';
import api from '../services/api';

export default function DiseaseHistory({ t, lang }) {
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [diseaseFilter, setDiseaseFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [selectedRecord, setSelectedRecord] = useState(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const [historyRes, statsRes] = await Promise.all([
        api.getDiseaseHistory({
          disease_filter: diseaseFilter !== 'all' ? diseaseFilter : undefined,
          severity_filter: severityFilter !== 'all' ? severityFilter : undefined,
          limit: 50
        }),
        api.getDiseaseStats()
      ]);
      setRecords(historyRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error('Error fetching disease history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [diseaseFilter, severityFilter]);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this scan record?')) return;
    try {
      await api.deleteDiseaseHistory(id);
      setRecords(records.filter(r => r.id !== id));
      if (selectedRecord?.id === id) setSelectedRecord(null);
    } catch (err) {
      console.error('Error deleting record:', err);
    }
  };

  const filteredRecords = records.filter(r => 
    r.disease.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.recommendation?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getSeverityBadge = (severity) => {
    const s = (severity || '').toLowerCase();
    if (s.includes('mild')) return 'badge-mild';
    if (s.includes('moderate')) return 'badge-moderate';
    if (s.includes('severe')) return 'badge-severe';
    return 'badge-healthy';
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
            {t.history.title}
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            {t.history.subtitle}
          </p>
        </div>

        <button
          onClick={fetchHistory}
          className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-3.5 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition-all shadow-sm"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* KPI Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="agri-card p-5">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {t.history.totalScans}
            </span>
            <p className="text-3xl font-black text-white mt-2">
              {stats.total_scans}
            </p>
          </div>
          <div className="agri-card p-5 border-emerald-500/30">
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
              {t.history.healthyCount}
            </span>
            <p className="text-3xl font-black text-emerald-400 mt-2">
              {stats.healthy_count}
            </p>
          </div>
          <div className="agri-card p-5 border-amber-500/30">
            <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
              {t.history.diseasedCount}
            </span>
            <p className="text-3xl font-black text-amber-400 mt-2">
              {stats.diseased_count}
            </p>
          </div>
        </div>
      )}

      {/* Search and Filters Bar */}
      <div className="agri-card p-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder={t.common.search}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-950/60 pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:border-emerald-500 focus:outline-none transition-all"
          />
        </div>

        {/* Dropdown Filters */}
        <div className="flex flex-wrap items-center gap-2">
          
          {/* Disease Filter */}
          <div className="flex items-center gap-1.5">
            <Filter className="h-3.5 w-3.5 text-slate-400" />
            <select
              value={diseaseFilter}
              onChange={(e) => setDiseaseFilter(e.target.value)}
              className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-xs text-slate-300 focus:border-emerald-500 focus:outline-none"
            >
              <option value="all">All Diseases</option>
              <option value="Bacterial_Spot">Bacterial Spot</option>
              <option value="Cercospora_Leaf_Spot">Cercospora Leaf Spot</option>
              <option value="Curl_Virus">Curl Virus</option>
              <option value="Healthy_Leaf">Healthy Leaf</option>
              <option value="Nutrition_Deficiency">Nutrition Deficiency</option>
              <option value="Powdery_Mildew">Powdery Mildew</option>
            </select>
          </div>

          {/* Severity Filter */}
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-xs text-slate-300 focus:border-emerald-500 focus:outline-none"
          >
            <option value="all">All Severities</option>
            <option value="mild">Mild</option>
            <option value="moderate">Moderate</option>
            <option value="severe">Severe</option>
            <option value="healthy">Healthy</option>
          </select>

        </div>
      </div>

      {/* History Grid / Table */}
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <RefreshCw className="h-8 w-8 animate-spin text-emerald-500" />
        </div>
      ) : filteredRecords.length === 0 ? (
        <div className="agri-card p-12 text-center">
          <History className="h-12 w-12 text-slate-600 mx-auto mb-3" />
          <p className="text-sm font-semibold text-slate-300">
            {t.history.noRecords}
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Perform leaf disease scans to build up your farm's pathology log.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredRecords.map((record) => {
            const isHealthy = record.disease === 'Healthy_Leaf';
            return (
              <div
                key={record.id}
                onClick={() => setSelectedRecord(record)}
                className="agri-card agri-card-hover p-4 cursor-pointer flex flex-col justify-between"
              >
                <div>
                  
                  {/* Image & Badges */}
                  <div className="relative aspect-video rounded-xl overflow-hidden bg-black/60 border border-slate-800 mb-3">
                    <img
                      src={record.image_url}
                      alt={record.disease}
                      className="h-full w-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=300&auto=format&fit=crop&q=60';
                      }}
                    />
                    <div className="absolute top-2 right-2">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md backdrop-blur-md ${getSeverityBadge(record.severity)}`}>
                        {record.severity}
                      </span>
                    </div>
                  </div>

                  {/* Disease Info */}
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-white">
                        {record.disease.replace(/_/g, ' ')}
                      </h3>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        {record.crop}
                      </p>
                    </div>
                    <span className="text-xs font-black text-emerald-400">
                      {record.confidence.toFixed(1)}%
                    </span>
                  </div>

                  {/* Recommendation Preview */}
                  <p className="text-xs text-slate-300 mt-2 line-clamp-2">
                    {record.recommendation}
                  </p>

                </div>

                {/* Bottom Actions & Date */}
                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <Calendar className="h-3.5 w-3.5" />
                    {new Date(record.created_at).toLocaleDateString()}
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => handleDelete(record.id, e)}
                      className="rounded-lg p-1.5 text-slate-500 hover:bg-red-500/10 hover:text-red-400 transition-colors"
                      title="Delete record"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                    <span className="text-emerald-400 hover:underline text-[11px] font-semibold">
                      {t.common.viewDetails} →
                    </span>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* Record Details Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="agri-card max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 relative border-emerald-500/40">
            
            <button
              onClick={() => setSelectedRecord(null)}
              className="absolute top-4 right-4 rounded-xl p-2 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="flex items-start gap-4 mb-4">
              <img
                src={selectedRecord.image_url}
                alt={selectedRecord.disease}
                className="h-24 w-24 rounded-xl object-cover border border-slate-700"
              />
              <div>
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                  Diagnostic Archive #{selectedRecord.id}
                </span>
                <h2 className="text-xl font-extrabold text-white mt-1">
                  {selectedRecord.disease.replace(/_/g, ' ')}
                </h2>
                <div className="flex items-center gap-2 mt-2">
                  <span className={`text-xs font-bold px-2.5 py-0.5 rounded-md ${getSeverityBadge(selectedRecord.severity)}`}>
                    {selectedRecord.severity}
                  </span>
                  <span className="text-xs font-semibold text-emerald-400">
                    Confidence: {selectedRecord.confidence.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-4 pt-4 border-t border-slate-800">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                  Cloudinary CDN Storage Asset
                </h4>
                <a
                  href={selectedRecord.image_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-sky-400 hover:underline flex items-center gap-1 break-all"
                >
                  <span>{selectedRecord.image_url}</span>
                  <ExternalLink className="h-3 w-3 shrink-0" />
                </a>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2">
                  Recorded Agronomic Recommendations
                </h4>
                <div className="rounded-xl bg-slate-950/80 p-4 border border-slate-800 text-xs sm:text-sm text-slate-200 whitespace-pre-line leading-relaxed">
                  {selectedRecord.recommendation}
                </div>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
                <span>Logged: {new Date(selectedRecord.created_at).toLocaleString()}</span>
                <span>Crop: {selectedRecord.crop}</span>
              </div>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
