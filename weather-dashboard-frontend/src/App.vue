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
          <div class="header-actions">
            <ThemeToggle />
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
import ThemeToggle from './components/ThemeToggle.vue'
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
    ThemeToggle,
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
  background-color: var(--color-background-secondary, #f8fafc);
}

/* Container Styles */
.container {
  max-width: var(--grid-containers-4xl, 1024px);
  padding: 0 var(--spacing-4, 1rem);
  margin: 0 auto;
}

/* Hero Header */
.hero-header {
  background: var(--gradient-primary, linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%));
  padding: var(--spacing-5, 1.25rem) 0;
  color: var(--color-text-inverse, #ffffff);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: inherit;
}

.header-actions {
  display: flex;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-3, 0.75rem);
}

.logo-icon {
  background-color: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-2, 0.5rem);
  border-radius: var(--radius-md, 0.375rem);
  display: flex;
  justify-content: center;
  align-items: center;
}

.cloud-icon {
  width: 40px;
  height: 40px;
  color: currentColor;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1, 0.25rem);
}

h1 {
  font-size: var(--text-2xl, 1.5rem);
  margin: 0;
  font-weight: var(--font-weight-semibold, 600);
  font-family: var(--font-display, inherit);
}

p {
  margin: 0;
  font-size: var(--text-sm, 0.875rem);
  opacity: 0.9;
}

/* Search Section */
.search-section {
  padding: var(--spacing-10, 2.5rem) 0;
}

.search-card {
  background: var(--color-surface-primary, #ffffff);
  border-radius: var(--radius-lg, 0.5rem);
  padding: var(--spacing-6, 1.5rem);
  box-shadow: var(--shadow-2, 0 4px 6px -1px rgb(0 0 0 / 0.1));
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid var(--color-border-primary, #e2e8f0);
}

.input-group {
  display: flex;
  align-items: center;
}

.input-icon {
  width: 24px;
  height: 24px;
  color: var(--color-primary-500, #3b82f6);
  margin-right: var(--spacing-2, 0.5rem);
}

.city-input {
  width: 100%;
  padding: var(--spacing-3, 0.75rem);
  border: 1px solid var(--color-border-primary, #e2e8f0);
  border-radius: var(--radius-md, 0.375rem) 0 0 var(--radius-md, 0.375rem);
  font-size: var(--text-base, 1rem);
  color: var(--color-text-primary, #0f172a);
  background-color: var(--color-surface-primary, #ffffff);
  min-width: 300px;
}

.search-btn {
  padding: var(--spacing-3, 0.75rem) var(--spacing-4, 1rem);
  background-color: var(--color-primary-500, #3b82f6);
  color: var(--color-text-inverse, #ffffff);
  font-size: var(--text-base, 1rem);
  font-weight: var(--font-weight-semibold, 600);
  border: none;
  border-radius: 0 var(--radius-md, 0.375rem) var(--radius-md, 0.375rem) 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-2, 0.5rem);
}

.search-btn:hover {
  background-color: var(--color-primary-600, #2563eb);
}

.search-btn:disabled {
  background-color: var(--color-neutral-400, #9ca3af);
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
  background: var(--color-error-100, #fee2e2);
  border-left: 4px solid var(--color-error-500, #ef4444);
  padding: var(--spacing-4, 1rem) var(--spacing-5, 1.25rem);
  border-radius: var(--radius-md, 0.375rem);
  margin: var(--spacing-5, 1.25rem) 0;
  display: flex;
  gap: var(--spacing-4, 1rem);
  align-items: center;
  border: 1px solid var(--color-error-200, #fecaca);
}

.error-icon {
  width: 32px;
  height: 32px;
  color: var(--color-error-500, #ef4444);
  flex-shrink: 0;
}

.error-content h3 {
  margin: 0;
  color: var(--color-error-600, #dc2626);
  font-weight: var(--font-weight-semibold, 600);
  font-size: var(--text-lg, 1.125rem);
}

.error-content p {
  margin: var(--spacing-1, 0.25rem) 0 0;
  color: var(--color-error-700, #b91c1c);
}

/* Weather Content */
.weather-content {
  display: grid;
  gap: var(--spacing-5, 1.25rem);
}

.current-weather {
  background-color: var(--color-surface-primary, #ffffff);
  padding: var(--spacing-6, 1.5rem) var(--spacing-8, 2rem);
  border-radius: var(--radius-lg, 0.5rem);
  display: grid;
  gap: var(--spacing-4, 1rem);
  box-shadow: var(--shadow-3, 0 10px 15px -3px rgb(0 0 0 / 0.1));
  border: 1px solid var(--color-border-primary, #e2e8f0);
}

.weather-main-card {
  display: grid;
  gap: var(--spacing-4, 1rem);
}

.weather-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.location h2 {
  font-size: var(--text-xl, 1.25rem);
  margin: 0;
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #0f172a);
}

.timestamp {
  font-size: var(--text-sm, 0.875rem);
  color: var(--color-text-secondary, #475569);
  margin-top: var(--spacing-1, 0.25rem);
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
  font-family: var(--font-display, inherit);
  font-size: var(--text-5xl, 3rem);
  font-weight: var(--font-weight-black, 900);
  color: var(--color-text-primary, #0f172a);
}

.temp-value {
  margin-right: var(--spacing-2, 0.5rem);
}

.temp-unit {
  font-size: 0.6em;
  font-weight: var(--font-weight-medium, 500);
}

.weather-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1, 0.25rem);
}

.description {
  font-size: var(--text-lg, 1.125rem);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-primary, #0f172a);
  text-transform: capitalize;
}

.feels-like {
  color: var(--color-text-secondary, #475569);
  font-size: var(--text-sm, 0.875rem);
}

.weather-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-4, 1rem);
  padding-top: var(--spacing-4, 1rem);
  border-top: 1px solid var(--color-border-primary, #e2e8f0);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-3, 0.75rem);
}

.stat-icon {
  width: 34px;
  height: 34px;
  color: var(--color-primary-500, #3b82f6);
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-0-5, 0.125rem);
}

.stat-value {
  display: block;
  font-size: var(--text-lg, 1.125rem);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #0f172a);
}

.stat-label {
  font-size: var(--text-xs, 0.75rem);
  color: var(--color-text-tertiary, #64748b);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide, 0.025em);
}
</style>

