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

      return {
        labels,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: this.forecasts.slice(0, 20).map(f => f.temperature),
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6
          },
          {
            label: 'Feels Like (°C)',
            data: this.forecasts.slice(0, 20).map(f => f.feels_like),
            borderColor: '#764ba2',
            backgroundColor: 'rgba(118, 75, 162, 0.1)',
            fill: false,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5,
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

      return {
        labels,
        datasets: [
          {
            label: 'Humidity (%)',
            data: this.forecasts.slice(0, 20).map(f => f.humidity),
            borderColor: '#4ecdc4',
            backgroundColor: 'rgba(78, 205, 196, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5
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

      return {
        labels,
        datasets: [
          {
            label: 'Wind Speed (m/s)',
            data: this.dailyForecasts.map(f => f.wind_speed),
            backgroundColor: 'rgba(102, 126, 234, 0.8)',
            yAxisID: 'y'
          },
          {
            label: 'Pressure (hPa)',
            data: this.dailyForecasts.map(f => f.pressure / 10), // Scale down for better visualization
            backgroundColor: 'rgba(78, 205, 196, 0.8)',
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
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05), 0 12px 24px -6px rgba(0, 0, 0, 0.1);
}

.charts-header {
  text-align: center;
  margin-bottom: 32px;
}

.charts-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.charts-header p {
  color: #6b7280;
  font-size: 0.95rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.chart-card {
  background: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.chart-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.chart-header h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.chart-icon {
  width: 20px;
  height: 20px;
  color: #667eea;
}

.chart-wrapper {
  height: 250px;
  position: relative;
}

/* Weather Timeline Styles */
.weather-timeline {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.timeline-date {
  font-weight: 600;
  color: #374151;
  min-width: 80px;
  font-size: 0.9rem;
}

.timeline-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.timeline-icon {
  width: 40px;
  height: 40px;
}

.timeline-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.timeline-temp {
  font-weight: 600;
  font-size: 1.1rem;
  color: #1f2937;
}

.timeline-desc {
  color: #6b7280;
  font-size: 0.9rem;
}

.timeline-pop {
  color: #3b82f6;
  font-size: 0.85rem;
  font-weight: 500;
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
