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
app.config.globalProperties.$apiBase = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

// Mount the app
app.mount('#app')
