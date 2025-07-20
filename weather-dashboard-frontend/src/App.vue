<template>
  <div class="app">
    <!-- Hero Header -->
    <header class="hero-header">
      <div class="container">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo-icon">
              <Cloud class="cloud-icon" />
            </div>
            <div class="header-text">
              <h1>Weather Dashboard</h1>
              <p>Beautiful weather data with interactive charts</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container">
        <!-- Search Section -->
        <section class="search-section">
          <div class="search-card">
            <div class="search-form">
              <div class="input-group">
                <MapPin class="input-icon" />
                <input
                  type="text"
                  v-model="city"
                  @keyup.enter="getWeatherData"
                  placeholder="Enter city name (e.g., London, New York)"
                  class="city-input"
                />
                <button 
                  @click="getWeatherData" 
                  :disabled="loading"
                  class="search-btn"
                >
                  <Search v-if="!loading" class="btn-icon" />
                  <Loader2 v-else class="btn-icon spin" />
                  {{ loading ? 'Loading...' : 'Get Weather' }}
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Error State -->
        <div v-if="error" class="error-card">
          <AlertCircle class="error-icon" />
          <div class="error-content">
            <h3>Oops! Something went wrong</h3>
            <p>{{ error }}</p>
          </div>
        </div>

        <!-- Weather Content -->
        <div v-if="weatherData && !loading && !error" class="weather-content">
          <!-- Current Weather Card -->
          <section class="current-weather">
            <div class="weather-main-card">
              <div class="weather-header">
                <div class="location">
                  <h2>{{ weatherData.city }}, {{ weatherData.country }}</h2>
                  <p class="timestamp">{{ formatTimestamp(weatherData.timestamp) }}</p>
                </div>
                <div class="weather-icon">
                  <img
                    :src="`https://openweathermap.org/img/wn/${weatherData.icon}@4x.png`"
                    :alt="weatherData.description"
                  />
                </div>
              </div>
              
              <div class="weather-main">
                <div class="temperature">
                  <span class="temp-value">{{ Math.round(weatherData.temperature) }}</span>
                  <span class="temp-unit">°C</span>
                </div>
                <div class="weather-details">
                  <p class="description">{{ capitalize(weatherData.description) }}</p>
                  <p class="feels-like">Feels like {{ Math.round(weatherData.feels_like) }}°C</p>
                </div>
              </div>

              <!-- Weather Stats Grid -->
              <div class="weather-stats">
                <div class="stat-item">
                  <div class="stat-icon">
                    <Droplets />
                  </div>
                  <div class="stat-content">
                    <span class="stat-value">{{ weatherData.humidity }}%</span>
                    <span class="stat-label">Humidity</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-icon">
                    <Gauge />
                  </div>
                  <div class="stat-content">
                    <span class="stat-value">{{ weatherData.pressure }} hPa</span>
                    <span class="stat-label">Pressure</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-icon">
                    <Wind />
                  </div>
                  <div class="stat-content">
                    <span class="stat-value">{{ weatherData.wind_speed }} m/s</span>
                    <span class="stat-label">Wind Speed</span>
                  </div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-icon">
                    <Eye />
                  </div>
                  <div class="stat-content">
                    <span class="stat-value">{{ weatherData.visibility }} km</span>
                    <span class="stat-label">Visibility</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Charts Section -->
          <section v-if="forecastData && forecastData.length" class="charts-section">
            <WeatherCharts :forecasts="forecastData" :city="weatherData.city" />
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import WeatherCharts from './components/WeatherCharts.vue'
import {
  Cloud,
  MapPin,
  Search,
  Loader2,
  AlertCircle,
  Droplets,
  Gauge,
  Wind,
  Eye
} from 'lucide-vue-next'

export default {
  name: 'WeatherDashboard',
  components: {
    WeatherCharts,
    Cloud,
    MapPin,
    Search,
    Loader2,
    AlertCircle,
    Droplets,
    Gauge,
    Wind,
    Eye
  },
  data() {
    return {
      city: 'London', // Default city for demo
      weatherData: null,
      forecastData: null,
      loading: false,
      error: ''
    }
  },
  mounted() {
    // Load default city weather on mount
    if (this.city) {
      this.getWeatherData()
    }
  },
  methods: {
    async getWeatherData() {
      if (!this.city?.trim()) {
        this.error = 'Please enter a city name'
        return
      }

      this.loading = true
      this.error = ''
      this.weatherData = null
      this.forecastData = null

      try {
        // Fetch current weather
        const weatherResponse = await axios.get(`${this.$apiBase}/api/weather`, {
          params: { city: this.city.trim() },
          timeout: 10000
        })

        if (weatherResponse.data.status === 'success') {
          this.weatherData = weatherResponse.data.data
        } else {
          throw new Error(weatherResponse.data.error || 'Failed to fetch weather data')
        }

        // Fetch forecast data
        const forecastResponse = await axios.get(`${this.$apiBase}/api/forecast`, {
          params: { city: this.city.trim(), days: 5 },
          timeout: 10000
        })

        if (forecastResponse.data.status === 'success') {
          this.forecastData = forecastResponse.data.data.forecasts
        }
      } catch (error) {
        console.error('Weather API Error:', error)
        if (error.code === 'ECONNABORTED') {
          this.error = 'Request timed out. Please try again.'
        } else if (error.response) {
          this.error = error.response.data?.error || `Server error: ${error.response.status}`
        } else if (error.request) {
          this.error = 'Unable to connect to weather service. Please check if the backend is running.'
        } else {
          this.error = error.message || 'An unexpected error occurred'
        }
      } finally {
        this.loading = false
      }
    },
    
    formatTimestamp(timestamp) {
      return new Date(timestamp * 1000).toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    capitalize(str) {
      return str.replace(/\b\w/g, l => l.toUpperCase())
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

/* Main Application Wrapper */
.app {
  min-height: 100vh;
  background-color: #f5f9ff;
}

/* Container Styles */
.container {
  max-width: 1024px;
  padding: 0 16px;
  margin: 0 auto;
}

/* Hero Header */
.hero-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 6px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cloud-icon {
  width: 40px;
  height: 40px;
  color: #fff;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

h1 {
  font-size: 1.8em;
  margin: 0;
  font-weight: 600;
}

p {
  margin: 0;
  font-size: 0.9em;
}

/* Search Section */
.search-section {
  padding: 40px 0;
}

.search-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-group {
  display: flex;
  align-items: center;
}

.input-icon {
  width: 24px;
  height: 24px;
  color: #667eea;
  margin-right: 8px;
}

.city-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px 0 0 8px;
  font-size: 1em;
  color: #333;
}

.search-btn {
  padding: 10px 16px;
  background-color: #667eea;
  color: white;
  font-size: 1em;
  font-weight: 600;
  border: none;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-btn:disabled {
  background-color: #b3c2f3;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.spin {
  animation: spin 1s infinite linear;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Error Card */
.error-card {
  background: #ffe2e2;
  border-left: 4px solid #ff6b6b;
  padding: 16px 20px;
  border-radius: 8px;
  margin: 20px 0;
  display: flex;
  gap: 16px;
  align-items: center;
}

.error-icon {
  width: 32px;
  height: 32px;
  color: #ff6b6b;
}

.error-content h3 {
  margin: 0;
  color: #ff6b6b;
  font-weight: 600;
}

.error-content p {
  margin: 4px 0 0;
}

/* Weather Content */
.weather-content {
  display: grid;
  gap: 20px;
}

.current-weather {
  background-color: white;
  padding: 24px 32px;
  border-radius: 8px;
  display: grid;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05), 0 12px 24px -6px rgba(0,0,0,0.1);
}

.weather-main-card {
  display: grid;
  gap: 16px;
}

.weather-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.location h2 {
  font-size: 1.5em;
  margin: 0;
  font-weight: 600;
}

.timestamp {
  font-size: 0.9em;
  color: #666;
}

.weather-icon img {
  width: 80px;
  height: 80px;
}

.weather-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.temperature {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  font-size: 2.4em;
  font-weight: 900;
}

.temp-value {
  margin-right: 8px;
}

.temp-unit {
  font-size: 0.6em;
  font-weight: 500;
}

.weather-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.feels-like {
  color: #444;
  font-size: 0.9em;
}

.weather-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-icon {
  width: 34px;
  height: 34px;
  color: #667eea;
}

.stat-value {
  display: block;
  font-size: 1.1em;
  font-weight: 600;
}

.stat-label {
  font-size: 0.8em;
  color: #666;
}
</style>

