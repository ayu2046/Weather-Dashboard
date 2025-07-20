import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Import Chart.js components with auto-registration
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js'

// Import theme composable
import { useTheme } from './composables/useTheme'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
)

// Initialize theme system
const { applyCSSVariables } = useTheme()
applyCSSVariables()

// Create Vue app
const app = createApp(App)

// Global properties for API base URL
const isDevelopment = import.meta.env.DEV
const defaultApiUrl = isDevelopment 
  ? 'http://127.0.0.1:5000' 
  : 'https://your-weather-backend-name.onrender.com' // Replace with your actual backend URL

app.config.globalProperties.$apiBase = import.meta.env.VITE_API_BASE_URL || defaultApiUrl

// Log API configuration for debugging
console.log('🌐 API Base URL:', app.config.globalProperties.$apiBase)
console.log('🔧 Environment:', import.meta.env.MODE)

// Mount the app
app.mount('#app')
