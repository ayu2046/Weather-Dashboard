<template>
  <div class="charts-container">
    <div class="charts-header">
      <h3>5-Day Weather Forecast for {{ city }}</h3>
      <p>Interactive charts showing temperature trends and weather conditions</p>
    </div>

    <div class="charts-grid">
      <!-- Temperature Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <h4>
            <Thermometer class="chart-icon" />
            Temperature Trend
          </h4>
        </div>
        <div class="chart-wrapper">
          <Line :data="temperatureData" :options="temperatureOptions" />
        </div>
      </div>

      <!-- Humidity Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <h4>
            <Droplets class="chart-icon" />
            Humidity Levels
          </h4>
        </div>
        <div class="chart-wrapper">
          <Line :data="humidityData" :options="humidityOptions" />
        </div>
      </div>

      <!-- Weather Conditions -->
      <div class="chart-card">
        <div class="chart-header">
          <h4>
            <CloudRain class="chart-icon" />
            Weather Conditions
          </h4>
        </div>
        <div class="weather-timeline">
          <div 
            v-for="(forecast, index) in dailyForecasts" 
            :key="index"
            class="timeline-item"
          >
            <div class="timeline-date">
              {{ formatDate(forecast.datetime) }}
            </div>
            <div class="timeline-content">
              <img 
                :src="`https://openweathermap.org/img/wn/${forecast.icon}@2x.png`"
                :alt="forecast.description"
                class="timeline-icon"
              />
              <div class="timeline-info">
                <span class="timeline-temp">{{ Math.round(forecast.temperature) }}°C</span>
                <span class="timeline-desc">{{ capitalize(forecast.description) }}</span>
                <span class="timeline-pop">{{ Math.round(forecast.pop) }}% rain</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Wind & Pressure Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <h4>
            <Wind class="chart-icon" />
            Wind Speed & Pressure
          </h4>
        </div>
        <div class="chart-wrapper">
          <Bar :data="windPressureData" :options="windPressureOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Line, Bar } from 'vue-chartjs'
import { Thermometer, Droplets, CloudRain, Wind } from 'lucide-vue-next'

export default {
  name: 'WeatherCharts',
  components: {
    Line,
    Bar,
    Thermometer,
    Droplets,
    CloudRain,
    Wind
  },
  props: {
    forecasts: {
      type: Array,
      required: true
    },
    city: {
      type: String,
      required: true
    }
  },
  computed: {
    // Get CSS variable color values
    themeColors() {
      const root = document.documentElement
      const getCSS = (varName, fallback) => {
        const value = getComputedStyle(root).getPropertyValue(varName).trim()
        return value || fallback
      }
      
      return {
        primary: getCSS('--color-primary-500', '#3b82f6'),
        secondary: getCSS('--color-secondary-500', '#0ea5e9'),
        accent: getCSS('--color-accent-500', '#e879f9'),
        success: getCSS('--color-success-500', '#22c55e'),
        warning: getCSS('--color-warning-500', '#f59e0b'),
        error: getCSS('--color-error-500', '#ef4444')
      }
    },
    
    // Group forecasts by day for timeline view
    dailyForecasts() {
      const days = {}
      this.forecasts.forEach(forecast => {
        const date = new Date(forecast.datetime * 1000)
        const dayKey = date.toDateString()
        
        if (!days[dayKey] || date.getHours() === 12) { // Prefer noon forecast
          days[dayKey] = forecast
        }
      })
      
      return Object.values(days).slice(0, 5) // Limit to 5 days
    },

    // Temperature chart data
    temperatureData() {
      const labels = this.forecasts.slice(0, 20).map(f => {
        const date = new Date(f.datetime * 1000)
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit'
        })
      })
      
      const primaryColor = this.themeColors.primary
      const secondaryColor = this.themeColors.secondary

      return {
        labels,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: this.forecasts.slice(0, 20).map(f => f.temperature),
            borderColor: primaryColor,
            backgroundColor: primaryColor + '20', // 20 is hex for ~12% opacity
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: primaryColor,
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          },
          {
            label: 'Feels Like (°C)',
            data: this.forecasts.slice(0, 20).map(f => f.feels_like),
            borderColor: secondaryColor,
            backgroundColor: secondaryColor + '20',
            fill: false,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: secondaryColor,
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            borderDash: [5, 5]
          }
        ]
      }
    },

    // Humidity chart data
    humidityData() {
      const labels = this.forecasts.slice(0, 20).map(f => {
        const date = new Date(f.datetime * 1000)
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit'
        })
      })
      
      const accentColor = this.themeColors.accent

      return {
        labels,
        datasets: [
          {
            label: 'Humidity (%)',
            data: this.forecasts.slice(0, 20).map(f => f.humidity),
            borderColor: accentColor,
            backgroundColor: accentColor + '20',
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: accentColor,
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          }
        ]
      }
    },

    // Wind and pressure chart data
    windPressureData() {
      const labels = this.dailyForecasts.map(f => {
        const date = new Date(f.datetime * 1000)
        return date.toLocaleDateString('en-US', {
          weekday: 'short',
          month: 'short',
          day: 'numeric'
        })
      })
      
      const primaryColor = this.themeColors.primary
      const secondaryColor = this.themeColors.secondary

      return {
        labels,
        datasets: [
          {
            label: 'Wind Speed (m/s)',
            data: this.dailyForecasts.map(f => f.wind_speed),
            backgroundColor: primaryColor + 'CC', // CC is hex for ~80% opacity
            borderColor: primaryColor,
            borderWidth: 1,
            yAxisID: 'y'
          },
          {
            label: 'Pressure (hPa ÷ 10)',
            data: this.dailyForecasts.map(f => f.pressure / 10), // Scale down for better visualization
            backgroundColor: secondaryColor + 'CC',
            borderColor: secondaryColor,
            borderWidth: 1,
            yAxisID: 'y1'
          }
        ]
      }
    },

    // Chart options
    temperatureOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${Math.round(context.raw)}°C`
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Temperature (°C)'
            }
          }
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false
        }
      }
    },

    humidityOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `Humidity: ${Math.round(context.raw)}%`
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Humidity (%)'
            },
            min: 0,
            max: 100
          }
        }
      }
    },

    windPressureOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Days'
            }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: 'Wind Speed (m/s)'
            }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: 'Pressure (hPa × 10)'
            },
            grid: {
              drawOnChartArea: false
            }
          }
        }
      }
    }
  },
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
      })
    },
    
    capitalize(str) {
      return str.replace(/\b\w/g, l => l.toUpperCase())
    }
  }
}
</script>

<style scoped>
.charts-container {
  background: var(--color-surface-primary, #ffffff);
  border-radius: var(--radius-xl, 0.75rem);
  padding: var(--spacing-6, 1.5rem);
  box-shadow: var(--shadow-3, 0 10px 15px -3px rgb(0 0 0 / 0.1));
  border: 1px solid var(--color-border-primary, #e2e8f0);
}

.charts-header {
  text-align: center;
  margin-bottom: var(--spacing-8, 2rem);
}

.charts-header h3 {
  font-size: var(--text-xl, 1.25rem);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #0f172a);
  margin-bottom: var(--spacing-2, 0.5rem);
  font-family: var(--font-display, inherit);
}

.charts-header p {
  color: var(--color-text-secondary, #475569);
  font-size: var(--text-sm, 0.875rem);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-6, 1.5rem);
}

.chart-card {
  background: var(--color-surface-secondary, #f8fafc);
  border-radius: var(--radius-md, 0.375rem);
  padding: var(--spacing-5, 1.25rem);
  border: 1px solid var(--color-border-secondary, #cbd5e1);
}

.chart-header {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-4, 1rem);
}

.chart-header h4 {
  display: flex;
  align-items: center;
  gap: var(--spacing-2, 0.5rem);
  font-size: var(--text-lg, 1.125rem);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #0f172a);
}

.chart-icon {
  width: 20px;
  height: 20px;
  color: var(--color-primary-500, #3b82f6);
}

.chart-wrapper {
  height: 250px;
  position: relative;
}

/* Weather Timeline Styles */
.weather-timeline {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4, 1rem);
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-4, 1rem);
  padding: var(--spacing-3, 0.75rem);
  background: var(--color-surface-primary, #ffffff);
  border-radius: var(--radius-md, 0.375rem);
  border: 1px solid var(--color-border-primary, #e2e8f0);
  transition: all var(--duration-200, 200ms) var(--timing-ease, ease);
}

.timeline-item:hover {
  box-shadow: var(--shadow-1, 0 1px 3px 0 rgb(0 0 0 / 0.1));
  transform: translateY(-1px);
}

.timeline-date {
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #0f172a);
  min-width: 80px;
  font-size: var(--text-sm, 0.875rem);
}

.timeline-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-3, 0.75rem);
  flex: 1;
}

.timeline-icon {
  width: 40px;
  height: 40px;
}

.timeline-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-0-5, 0.125rem);
}

.timeline-temp {
  font-weight: var(--font-weight-semibold, 600);
  font-size: var(--text-lg, 1.125rem);
  color: var(--color-text-primary, #0f172a);
}

.timeline-desc {
  color: var(--color-text-secondary, #475569);
  font-size: var(--text-sm, 0.875rem);
  text-transform: capitalize;
}

.timeline-pop {
  color: var(--color-primary-500, #3b82f6);
  font-size: var(--text-xs, 0.75rem);
  font-weight: var(--font-weight-medium, 500);
}

/* Responsive Design */
@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .chart-card {
    padding: 16px;
  }
  
  .chart-wrapper {
    height: 200px;
  }
  
  .timeline-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .timeline-content {
    width: 100%;
  }
}
</style>
