import React, { useState, useRef } from 'react';
import { 
  UploadCloud, ScanEye, CheckCircle2, AlertTriangle, 
  ExternalLink, Sparkles, RefreshCw, Info, FileImage, ShieldAlert
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell 
} from 'recharts';
import api from '../services/api';

export default function DiseaseDetection({ t, lang }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = (file) => {
    if (!file) return;
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('Please upload a valid image file (JPG, PNG, WEBP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image file size exceeds 10 MB limit.');
      return;
    }
    setError(null);
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    try {
      setLoading(true);
      setError(null);
      const formData = new FormData();
      formData.append('file', selectedFile);

      const res = await api.predictDisease(formData);
      setResult(res.data);
    } catch (err) {
      console.error('Detection error:', err);
      setError(err.response?.data?.detail || 'Failed to analyze leaf image. Please check backend connection.');
    } finally {
      setLoading(false);
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  // Format probabilities for chart
  const chartData = result?.all_probabilities
    ? Object.entries(result.all_probabilities).map(([name, prob]) => ({
        name: name.replace(/_/g, ' '),
        prob: prob,
        rawName: name
      }))
    : [];

  const getSeverityBadgeClass = (severity) => {
    if (!severity) return 'badge-healthy';
    if (severity.toLowerCase().includes('mild')) return 'badge-mild';
    if (severity.toLowerCase().includes('moderate')) return 'badge-moderate';
    if (severity.toLowerCase().includes('severe')) return 'badge-severe';
    return 'badge-healthy';
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
          {t.disease.title}
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          {t.disease.subtitle}
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-300 flex items-center gap-3">
          <AlertTriangle className="h-5 w-5 text-red-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Upload Dropzone Section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        
        {/* Dropzone Column */}
        <div className={result ? "lg:col-span-5" : "lg:col-span-12"}>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => !previewUrl && fileInputRef.current?.click()}
            className={`agri-card p-6 border-2 border-dashed flex flex-col items-center justify-center text-center cursor-pointer transition-all ${
              dragActive 
                ? 'border-emerald-500 bg-emerald-500/10' 
                : 'border-slate-800 hover:border-slate-700'
            } ${previewUrl ? 'cursor-default' : ''}`}
            style={{ minHeight: result ? '340px' : '260px' }}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={(e) => handleFile(e.target.files[0])}
              className="hidden"
            />

            {!previewUrl ? (
              <div className="space-y-3 py-6">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-400">
                  <UploadCloud className="h-8 w-8" />
                </div>
                <div>
                  <p className="text-base font-bold text-white">
                    {t.disease.dropzoneTitle}
                  </p>
                  <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                    {t.disease.dropzoneHint}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}
                  className="rounded-xl bg-slate-800 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-700 transition-all"
                >
                  Browse Files
                </button>
              </div>
            ) : (
              <div className="w-full space-y-4">
                <div className="relative rounded-xl overflow-hidden border border-slate-700 bg-black/40 max-h-72 flex items-center justify-center">
                  <img
                    src={previewUrl}
                    alt="Chilli Leaf Preview"
                    className="max-h-72 w-auto object-contain rounded-lg shadow-inner"
                  />
                  {loading && (
                    <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm flex flex-col items-center justify-center gap-3">
                      <RefreshCw className="h-8 w-8 animate-spin text-emerald-400" />
                      <p className="text-xs font-semibold text-emerald-300">
                        {t.disease.uploading}
                      </p>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleAnalyze}
                    disabled={loading}
                    className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-sm font-bold text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-950/40 disabled:opacity-50"
                  >
                    <ScanEye className="h-4 w-4" />
                    <span>{loading ? t.common.loading : t.disease.detectButton}</span>
                  </button>

                  <button
                    onClick={resetUpload}
                    disabled={loading}
                    className="rounded-xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm font-semibold text-slate-400 hover:bg-slate-800 hover:text-white transition-all"
                  >
                    {t.common.cancel}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Results Column */}
        {result && (
          <div className="lg:col-span-7 space-y-6">
            
            {/* Main Result Card */}
            <div className="agri-card p-6 border-emerald-500/30">
              
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                    {t.disease.detectionResult}
                  </span>
                  <h2 className="text-2xl font-black text-white mt-1">
                    {result.disease_display_name}
                  </h2>
                  <p className="text-xs text-slate-400 italic mt-0.5">
                    {result.scientific_name}
                  </p>
                </div>

                <div className="text-right">
                  <span className="text-xs font-semibold text-slate-400 block">
                    {t.disease.confidenceScore}
                  </span>
                  <span className="text-2xl font-black text-emerald-400">
                    {result.confidence.toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Severity & Cloudinary Row */}
              <div className="grid grid-cols-2 gap-3 py-4 border-b border-slate-800">
                
                {/* Prototype Severity */}
                <div className="rounded-xl bg-slate-900/60 p-3 border border-slate-800">
                  <span className="text-[11px] font-semibold text-slate-400 block mb-1">
                    {t.disease.severityAnalysis}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-extrabold px-2.5 py-1 rounded-md ${getSeverityBadgeClass(result.severity)}`}>
                      {result.severity}
                    </span>
                    {result.lesion_coverage_percent > 0 && (
                      <span className="text-xs text-slate-400">
                        (~{result.lesion_coverage_percent}% coverage)
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-slate-500 block mt-1.5 leading-tight">
                    {result.severity_method}
                  </span>
                </div>

                {/* Cloudinary Storage Link */}
                <div className="rounded-xl bg-slate-900/60 p-3 border border-slate-800 flex flex-col justify-between">
                  <div>
                    <span className="text-[11px] font-semibold text-slate-400 block mb-1">
                      Cloud Image Storage
                    </span>
                    <span className="text-xs text-sky-400 font-semibold flex items-center gap-1">
                      {t.common.uploadCloudinary}
                    </span>
                  </div>
                  {result.image_url && (
                    <a
                      href={result.image_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] text-slate-400 hover:text-white mt-1"
                    >
                      <span>{t.common.viewOnCloudinary}</span>
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>

              </div>

              {/* Pathology Description */}
              <div className="py-4 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  {t.disease.description}
                </h3>
                <p className="text-sm text-slate-200 leading-relaxed">
                  {result.description?.[lang] || result.description?.en}
                </p>
              </div>

              {/* Agronomic Recommendations */}
              <div className="pt-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-1.5">
                  <Sparkles className="h-4 w-4" />
                  <span>{t.disease.actionPlan}</span>
                </h3>
                
                <ul className="space-y-2">
                  {(result.recommendations_list?.[lang] || result.recommendations_list?.en || []).map((rec, idx) => (
                    <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-300">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>

            {/* Class Probabilities Distribution */}
            {chartData.length > 0 && (
              <div className="agri-card p-5">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                  Softmax Probability Distribution Across 6 Classes
                </h3>
                <div className="h-44 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 20, left: 80, bottom: 0 }}>
                      <XAxis type="number" domain={[0, 100]} unit="%" stroke="#475569" fontSize={10} />
                      <YAxis type="category" dataKey="name" stroke="#cbd5e1" fontSize={11} width={80} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem', color: '#fff' }}
                        formatter={(val) => [`${val}%`, 'Probability']}
                      />
                      <Bar dataKey="prob" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={entry.rawName === result.disease ? '#10b981' : '#334155'} 
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

          </div>
        )}

      </div>

    </div>
  );
}
