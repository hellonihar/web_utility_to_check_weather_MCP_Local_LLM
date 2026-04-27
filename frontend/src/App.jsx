import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cloud, MapPin, Wind, Droplets, Thermometer, Send, Search } from 'lucide-react';
import './App.css';

const App = () => {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://localhost:8001/api/cities')
      .then(res => res.json())
      .then(data => setCities(data.cities))
      .catch(err => console.error("Failed to fetch cities", err));
  }, []);

  const handleFetchWeather = async () => {
    if (!selectedCity) return;
    
    setLoading(true);
    setError('');
    setWeatherData(null);

    try {
      const response = await fetch('http://localhost:8001/api/weather', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city: selectedCity }),
      });

      if (!response.ok) throw new Error('Failed to fetch weather data');
      
      const data = await response.json();
      setWeatherData(data);
    } catch (err) {
      setError('Connection to backend failed. Make sure the backend server is running on port 8001.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="logo"
        >
          <Cloud className="icon-cyan" size={32} />
          <h1 className="gradient-text">SkyMCP</h1>
        </motion.div>
        <p className="subtitle">AI-Powered Weather Intel via Model Context Protocol</p>
      </header>

      <main>
        <section className="search-section">
          <div className="glass-card search-container">
            <div className="input-wrapper">
              <MapPin className="input-icon" size={20} />
              <select 
                value={selectedCity} 
                onChange={(e) => setSelectedCity(e.target.value)}
                className="city-select"
              >
                <option value="" disabled>Select a popular city...</option>
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>
            <button 
              onClick={handleFetchWeather} 
              disabled={loading || !selectedCity}
              className="fetch-button"
            >
              {loading ? (
                <div className="loader"></div>
              ) : (
                <>
                  <Search size={18} />
                  <span>Show Weather</span>
                </>
              )}
            </button>
          </div>
        </section>

        <section className="result-section">
          <AnimatePresence mode="wait">
            {error && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="error-message glass-card"
              >
                {error}
              </motion.div>
            )}

            {weatherData && (
              <motion.div 
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -30 }}
                transition={{ type: "spring", damping: 20 }}
                className="weather-card glass-card"
              >
                <div className="card-header">
                  <h2 className="city-name">{weatherData.city}</h2>
                  <div className="badge">Gemma 4 Intel</div>
                </div>
                
                <div className="llm-response">
                  <p>{weatherData.response}</p>
                </div>

                <div className="stats-grid">
                  <div className="stat-item">
                    <Thermometer size={20} className="icon-cyan" />
                    <span>Real-time Sync</span>
                  </div>
                  <div className="stat-item">
                    <Droplets size={20} className="icon-purple" />
                    <span>MCP Secured</span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </main>

      <footer>
        <p>© 2024 SkyMCP • Built with Ollama & Model Context Protocol</p>
      </footer>
    </div>
  );
};

export default App;
