import axios from 'axios';

const API_BASE = '/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const api = {
  // =====================================================
  // Dashboard
  // =====================================================

  getDashboardSummary: () =>
    apiClient.get('/dashboard/summary'),

  getUserProfile: () =>
    apiClient.get('/auth/profile'),


  // =====================================================
  // Disease Detection
  // =====================================================

  predictDisease: (formData) => {
    return apiClient.post('/disease/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getDiseaseHistory: (params) =>
    apiClient.get('/disease/history', { params }),

  deleteDiseaseHistory: (id) =>
    apiClient.delete(`/disease/history/${id}`),

  getDiseaseStats: () =>
    apiClient.get('/disease/stats'),


  // =====================================================
  // IoT Telemetry
  // =====================================================

  getLatestIoT: () =>
    apiClient.get('/iot/latest'),

  getIoTHistory: (params) =>
    apiClient.get('/iot/history', { params }),

  toggleIoTDemo: (enabled) =>
    apiClient.post(`/iot/toggle-demo?enabled=${enabled}`),

  sendIoTSensorData: (data) =>
    apiClient.post('/iot/sensor-data', data),

  // Water pump control
  getPumpStatus: () =>
    apiClient.get('/iot/pump'),

  setPump: (state) =>
    apiClient.post(`/iot/pump?state=${state}`),


  // =====================================================
  // Smart Irrigation
  // =====================================================

  calculateIrrigation: (data) =>
    apiClient.post('/irrigation/calculate', data),

  getIrrigationHistory: () =>
    apiClient.get('/irrigation/history'),


  // =====================================================
  // Soil Health
  // =====================================================

  analyzeSoil: (data) =>
    apiClient.post('/soil/analyze', data),

  getSoilRecords: () =>
    apiClient.get('/soil/records'),


  // =====================================================
  // Crop Recommendation
  // =====================================================

  recommendCrops: (data) =>
    apiClient.post('/crop/recommend', data),


  // =====================================================
  // Weather
  // =====================================================

  // Current weather
  // Example:
  // api.getWeatherCurrent({
  //   lat: 16.7090,
  //   lon: 74.4561
  // })

  getWeatherCurrent: (params) =>
    apiClient.get('/weather/current', { params }),

  // Weather forecast
  // Example:
  // api.getWeatherForecast({
  //   lat: 16.7090,
  //   lon: 74.4561
  // })

  getWeatherForecast: (params) =>
    apiClient.get('/weather/forecast', { params }),


  // =====================================================
  // AI Chat
  // =====================================================

  sendChatMessage: (data) =>
    apiClient.post('/chat', data),
};

export default api;