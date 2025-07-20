# Weather Dashboard Frontend

A beautiful, responsive Vue.js frontend for the Weather Dashboard application with interactive charts and modern design.

## 🌟 Features

- **Modern Vue 3 Composition API**
- **Interactive Charts** powered by Chart.js
- **Responsive Design** that works on all devices
- **Beautiful UI** with gradient backgrounds and smooth animations
- **Real-time Weather Data** from OpenWeather API
- **5-Day Forecast** with detailed charts
- **Weather Statistics** with intuitive icons
- **Error Handling** with user-friendly messages

## 🚀 Technologies Used

- **Vue.js 3** - Modern JavaScript framework
- **Vite** - Fast build tool and dev server
- **Chart.js** - Interactive charts and graphs
- **vue-chartjs** - Vue.js wrapper for Chart.js
- **Lucide Vue** - Beautiful icon library
- **Axios** - HTTP client for API requests

## 📦 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd weather-dashboard-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   - Edit the `.env` file to match your backend API URL
   - Default is set to `http://127.0.0.1:5000`

4. **Start the development server:**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint and fix code issues

## 📁 Project Structure

```
weather-dashboard-frontend/
├── src/
│   ├── components/
│   │   └── WeatherCharts.vue      # Chart components with Chart.js
│   ├── App.vue                    # Main application component
│   ├── main.js                    # Application entry point
│   └── style.css                  # Global styles
├── public/                        # Static assets
├── index.html                     # HTML template
├── package.json                   # Dependencies and scripts
├── vite.config.js                # Vite configuration
└── README.md                      # This file
```

## 🎨 UI Components

### Main Dashboard
- **Header Section** - App branding with gradient background
- **Search Section** - City input with beautiful form controls
- **Current Weather Card** - Large temperature display with weather stats
- **Charts Section** - Interactive weather forecast charts

### Charts Included
1. **Temperature Trend** - Line chart showing temperature over time
2. **Humidity Levels** - Area chart for humidity tracking
3. **Weather Conditions** - Visual timeline with weather icons
4. **Wind & Pressure** - Dual-axis bar chart

## 🔌 API Integration

The frontend connects to the Flask backend API:

- **Current Weather**: `GET /api/weather?city={city}`
- **Weather Forecast**: `GET /api/forecast?city={city}&days=5`
- **Health Check**: `GET /api/health`

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop** (1024px+)
- **Tablet** (768px - 1023px)
- **Mobile** (< 768px)

## 🎯 Key Features

### Interactive Charts
- Responsive charts that adapt to screen size
- Hover effects and tooltips
- Multiple data series support
- Smooth animations

### Weather Data Visualization
- Temperature trends over 5 days
- Humidity percentage tracking
- Wind speed and pressure correlations
- Weather condition timeline

### Error Handling
- Network error detection
- API timeout handling
- User-friendly error messages
- Loading states with spinners

## 🔧 Configuration

### Environment Variables
- `VITE_API_BASE_URL` - Backend API URL
- `VITE_APP_NAME` - Application name
- `VITE_APP_VERSION` - Application version

### Development Setup
1. Ensure the backend API is running on port 5000
2. Install Node.js (version 16 or higher)
3. Run `npm install` to install dependencies
4. Use `npm run dev` for development

## 🚀 Production Build

To build for production:

```bash
npm run build
```

This creates an optimized build in the `dist/` directory that can be served by any static file server.

## 🤝 Integration with Backend

Make sure the Flask backend is running before starting the frontend. The default configuration expects the backend to be available at `http://127.0.0.1:5000`.

## 📄 License

This project is part of the Weather Dashboard application and is available under the MIT License.
