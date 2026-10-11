import React, { useState, useEffect } from 'react';

import {
  CloudSun,
  Sun,
  CloudRain,
  Wind,
  Droplets,
  AlertTriangle,
  RefreshCw,
  MapPin,
  Navigation
} from 'lucide-react';

import api from '../services/api';


export default function WeatherPage({ t, lang }) {

  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationError, setLocationError] = useState('');


  // =====================================================
  // GET WEATHER USING CURRENT BROWSER LOCATION
  // =====================================================

  const fetchWeather = async () => {

    setLoading(true);
    setLocationLoading(true);
    setLocationError('');

    try {

      // -------------------------------------------------
      // Check browser geolocation support
      // -------------------------------------------------

      if (!navigator.geolocation) {

        setLocationError(
          'Geolocation is not supported by your browser.'
        );

        setLoading(false);
        setLocationLoading(false);

        return;
      }


      // -------------------------------------------------
      // Get current GPS coordinates
      // -------------------------------------------------

      navigator.geolocation.getCurrentPosition(

        async (position) => {

          try {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;


            console.log(
              'Current GPS Location:',
              latitude,
              longitude
            );


            // -------------------------------------------------
            // Send GPS coordinates to backend
            // -------------------------------------------------

            const response =
              await api.getWeatherForecast({
                lat: latitude,
                lon: longitude
              });


            console.log(
              'Weather API Response:',
              response.data
            );


            // -------------------------------------------------
            // Store weather
            // -------------------------------------------------

            setWeatherData(response.data);

          } catch (error) {

            console.error(
              'Weather API error:',
              error
            );


            // Show backend error if available

            const backendMessage =
              error?.response?.data?.detail ||
              error?.response?.data?.message;

            setLocationError(
              backendMessage ||
              'Unable to fetch weather for your current location.'
            );

          } finally {

            setLoading(false);
            setLocationLoading(false);

          }

        },


        // -------------------------------------------------
        // GEOLOCATION ERROR
        // -------------------------------------------------

        (error) => {

          console.error(
            'Geolocation error:',
            error
          );


          let message =
            'Unable to determine your current location.';


          switch (error.code) {

            case error.PERMISSION_DENIED:

              message =
                'Location permission was denied. Please allow location access in your browser and try again.';

              break;


            case error.POSITION_UNAVAILABLE:

              message =
                'Your current location is unavailable. Please check your device location settings.';

              break;


            case error.TIMEOUT:

              message =
                'Location request timed out. Please try again.';

              break;


            default:

              message =
                'Unable to determine your current location.';
          }


          setLocationError(message);

          setLoading(false);
          setLocationLoading(false);

        },


        // -------------------------------------------------
        // GEOLOCATION OPTIONS
        // -------------------------------------------------

        {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 300000
        }

      );

    } catch (error) {

      console.error(
        'Weather location error:',
        error
      );


      setLocationError(
        'Unable to load weather information.'
      );

      setLoading(false);
      setLocationLoading(false);

    }

  };


  // =====================================================
  // LOAD WEATHER WHEN PAGE OPENS
  // =====================================================

  useEffect(() => {

    fetchWeather();

  }, []);


  // =====================================================
  // LOADING SCREEN
  // =====================================================

  if (loading) {

    return (

      <div className="space-y-6 max-w-5xl mx-auto">

        <div>

          <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
            {t.weather.title}
          </h1>

          <p className="text-sm text-slate-400 mt-1">
            {t.weather.subtitle}
          </p>

        </div>


        <div className="agri-card p-10 border-emerald-500/30">

          <div className="flex flex-col items-center justify-center text-center">

            <Navigation
              className="h-10 w-10 text-emerald-400 animate-pulse mb-4"
            />


            <h2 className="text-lg font-bold text-white">

              {locationLoading
                ? 'Detecting your current location...'
                : 'Loading weather...'}

            </h2>


            <p className="text-sm text-slate-400 mt-2">

              Please allow location access to get weather for your current location.

            </p>

          </div>

        </div>

      </div>

    );

  }


  // =====================================================
  // WEATHER NOT AVAILABLE
  // =====================================================

  if (!weatherData || !weatherData.current) {

    return (

      <div className="space-y-6 max-w-5xl mx-auto">

        <div className="flex items-center justify-between">

          <div>

            <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
              {t.weather.title}
            </h1>

            <p className="text-sm text-slate-400 mt-1">
              {t.weather.subtitle}
            </p>

          </div>


          <button
            onClick={fetchWeather}
            className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-3.5 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white"
          >

            <RefreshCw className="h-3.5 w-3.5" />

            <span>Refresh</span>

          </button>

        </div>


        <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-5 text-sm text-red-300">

          <div className="flex items-start gap-3">

            <AlertTriangle
              className="h-5 w-5 text-red-400 shrink-0"
            />

            <div>

              <p className="font-bold">
                Weather unavailable
              </p>

              <p className="mt-1">
                {locationError ||
                  'Unable to load weather information.'}
              </p>

            </div>

          </div>

        </div>

      </div>

    );

  }


  // =====================================================
  // WEATHER DATA
  // =====================================================

  const current = weatherData.current;


  // =====================================================
  // MAIN UI
  // =====================================================

  return (

    <div className="space-y-6 max-w-5xl mx-auto">


      {/* =================================================
          HEADER
      ================================================= */}

      <div className="flex items-center justify-between">

        <div>

          <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl">
            {t.weather.title}
          </h1>

          <p className="text-sm text-slate-400 mt-1">
            {t.weather.subtitle}
          </p>

        </div>


        <button
          onClick={fetchWeather}
          disabled={loading}
          className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-3.5 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white disabled:opacity-50"
        >

          <RefreshCw
            className={`h-3.5 w-3.5 ${
              loading ? 'animate-spin' : ''
            }`}
          />

          <span>
            Refresh
          </span>

        </button>

      </div>


      {/* =================================================
          LOCATION ERROR
      ================================================= */}

      {locationError && (

        <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 p-4 text-xs sm:text-sm text-amber-300">

          <div className="flex items-start gap-3">

            <AlertTriangle
              className="h-5 w-5 text-amber-400 shrink-0"
            />

            <div>

              <span className="font-bold block">
                Location
              </span>

              <span>
                {locationError}
              </span>

            </div>

          </div>

        </div>

      )}


      {/* =================================================
          AGRICULTURAL ALERT
      ================================================= */}

      {current.agricultural_alert && (

        <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 p-4 text-xs sm:text-sm text-amber-300">

          <div className="flex items-start gap-3">

            <AlertTriangle
              className="h-5 w-5 text-amber-400 shrink-0 mt-0.5"
            />

            <div>

              <span className="font-bold block">
                {t.weather.alertTitle}:
              </span>

              <span>
                {current.agricultural_alert}
              </span>

            </div>

          </div>

        </div>

      )}


      {/* =================================================
          CURRENT WEATHER
      ================================================= */}

      <div className="agri-card p-6 border-emerald-500/30">

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">


          {/* LOCATION + TEMPERATURE */}

          <div>

            <div className="flex items-center gap-2">

              <MapPin
                className="h-4 w-4 text-emerald-400"
              />

              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">

                {current.location}

              </span>

            </div>


            <div className="flex items-baseline gap-4 mt-2">

              <span className="text-5xl font-black text-white">

                {current.temperature_c}°C

              </span>


              <span className="text-lg font-bold text-slate-300">

                {current.weather_condition}

              </span>

            </div>


            <p className="text-xs text-slate-400 mt-1">

              {lang === 'mr'
                ? current.forecast_summary_mr
                : current.forecast_summary_en}

            </p>

          </div>


          {/* =================================================
              WEATHER METRICS
          ================================================= */}

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">


            {/* FEELS LIKE */}

            <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">

              <span className="text-[11px] text-slate-400 block">

                {t.weather.feelsLike}

              </span>


              <span className="text-base font-black text-white">

                {current.feels_like_c}°C

              </span>

            </div>


            {/* HUMIDITY */}

            <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">

              <div className="flex items-center gap-1">

                <Droplets
                  className="h-3 w-3 text-teal-400"
                />

                <span className="text-[11px] text-slate-400">

                  {t.dashboard.humidity}

                </span>

              </div>


              <span className="text-base font-black text-teal-400">

                {current.humidity_percent}%

              </span>

            </div>


            {/* WIND */}

            <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">

              <div className="flex items-center gap-1">

                <Wind
                  className="h-3 w-3 text-blue-400"
                />

                <span className="text-[11px] text-slate-400">

                  {t.weather.windSpeed}

                </span>

              </div>


              <span className="text-base font-black text-blue-400">

                {current.wind_speed_kmh} km/h

              </span>

            </div>


            {/* RAIN */}

            <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">

              <div className="flex items-center gap-1">

                <CloudRain
                  className="h-3 w-3 text-purple-400"
                />

                <span className="text-[11px] text-slate-400">

                  {t.weather.rainProb}

                </span>

              </div>


              <span className="text-base font-black text-purple-400">

                {current.rain_probability_percent}%

              </span>

            </div>

          </div>

        </div>

      </div>

    </div>

  );

}