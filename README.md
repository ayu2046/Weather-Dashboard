# 🌤️ Weather Dashboard

A beautiful, full-stack weather dashboard application with interactive charts, forecasts, and location-based weather data visualization. Built with modern technologies and a focus on user experience.

![Weather Dashboard Preview](https://via.placeholder.com/800x400/667eea/FFFFFF?text=Weather+Dashboard+Preview)

## ✨ Features

### 🎯 Core Functionality
- **Real-time Weather Data** - Current weather conditions for any city
- **5-Day Forecast** - Detailed weather predictions with 3-hour intervals
- **Interactive Charts** - Temperature, humidity, wind speed, and pressure visualizations
- **Weather Alerts** - Notifications for severe weather conditions (requires premium API)
- **Location Search** - Easy city search with autocomplete suggestions

### 🎨 User Experience
- **Modern UI Design** - Clean, intuitive interface with gradient backgrounds
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Loading States** - Smooth loading animations and progress indicators
- **Error Handling** - User-friendly error messages and recovery options
- **Accessibility** - Screen reader compatible with proper ARIA labels

### 📊 Data Visualization
- **Temperature Trends** - Line charts showing temperature changes over time
- **Humidity Tracking** - Area charts for humidity percentage monitoring
- **Weather Timeline** - Visual timeline with weather icons and conditions
- **Wind & Pressure** - Dual-axis bar charts for atmospheric data

## 🚀 Technology Stack

### Backend (Python/Flask)
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Requests** - HTTP library for API calls
- **Python-dotenv** - Environment variable management
- **OpenWeather API** - Weather data source

### Frontend (Vue.js)
- **Vue.js 3** - Modern JavaScript framework with Composition API
- **Vite** - Fast build tool and development server
- **Chart.js** - Interactive charts and data visualization
- **Vue-ChartJS** - Vue.js wrapper for Chart.js
- **Lucide Vue** - Beautiful icon library
- **Axios** - HTTP client for API requests

## 📁 Project Structure

```
Weather Dashboard/
├── weather-dashboard-backend/          # Python Flask API
│   ├── app/
│   │   ├── __init__.py                # Flask app factory
│   │   ├── routes.py                  # API endpoints
│   │   └── services.py                # Weather service logic
│   ├── docs/                          # API documentation
│   ├── config.py                      # Configuration management
│   ├── run.py                         # Application entry point
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # Backend documentation
├── weather-dashboard-frontend/         # Vue.js Frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── WeatherCharts.vue     # Chart components
│   │   ├── App.vue                   # Main application
│   │   ├── main.js                   # Entry point
│   │   └── style.css                 # Global styles
│   ├── public/                       # Static assets
│   ├── package.json                  # Node.js dependencies
│   ├── vite.config.js               # Vite configuration
│   └── README.md                    # Frontend documentation
├── venv/                            # Python virtual environment
├── requirements.txt                 # Root Python dependencies
└── README.md                       # This file
```

## 🛠️ Quick Start

### Prerequisites
- **Python 3.7+** installed
- **Node.js 16+** and npm installed
- **OpenWeather API key** (free from [openweathermap.org](https://openweathermap.org/api))

### 1. Clone and Setup

```bash
# Clone the project
git clone <repository-url>
cd Weather\ Dashboard

# Setup Python virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Backend

```bash
cd weather-dashboard-backend

# Configure environment variables
# Edit .env file and add your OpenWeather API key:
echo "OPENWEATHER_API_KEY=your_actual_api_key_here" > .env

# Start the Flask backend
python run.py
```

The backend will be running at `http://127.0.0.1:5000`

### 3. Setup Frontend

```bash
# In a new terminal
cd weather-dashboard-frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Backend Configuration

Edit `weather-dashboard-backend/.env`:

```env
# Required
OPENWEATHER_API_KEY=your_32_character_api_key

# Optional (with defaults)
DEBUG=True
HOST=127.0.0.1
PORT=5000
API_TIMEOUT=10
DEFAULT_UNITS=metric
CORS_ORIGINS=*
```

### Frontend Configuration

Edit `weather-dashboard-frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
VITE_APP_NAME=Weather Dashboard
VITE_APP_VERSION=1.0.0
```

## 📡 API Endpoints

### Health Check
- `GET /api/health` - API status and version

### Current Weather
- `GET /api/weather?city=<city_name>` - Current weather data

### Weather Forecast
- `GET /api/forecast?city=<city_name>&days=<1-5>` - Weather forecast

### Weather Alerts
- `GET /api/alerts?city=<city_name>` - Weather alerts (premium feature)

## 📊 Charts and Visualizations

### Temperature Chart
- Line chart showing temperature trends
- Includes "feels like" temperature comparison
- Interactive tooltips with detailed information

### Humidity Chart
- Area chart displaying humidity levels over time
- Percentage-based visualization (0-100%)
- Color-coded for easy interpretation

### Weather Timeline
- Visual timeline with weather icons
- Daily weather conditions summary
- Precipitation probability indicators

### Wind & Pressure Chart
- Dual-axis bar chart
- Wind speed in m/s
- Atmospheric pressure in hPa

## 🌐 Deployment

### Backend Deployment (Production)

```bash
# Set production environment
export FLASK_ENV=production
export DEBUG=False

# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 run:app
```

### Frontend Deployment

```bash
# Build for production
npm run build

# The dist/ folder contains the built application
# Deploy to any static hosting service
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify your OpenWeather API key is valid
   - Check if the key is properly set in `.env`
   - Free keys may take up to 2 hours to activate

2. **Frontend Can't Connect to Backend**
   - Ensure backend is running on port 5000
   - Check `VITE_API_BASE_URL` in frontend `.env`
   - Verify CORS settings in backend configuration

3. **Charts Not Displaying**
   - Check browser console for JavaScript errors
   - Ensure Chart.js dependencies are properly installed
   - Verify forecast data is being received from API

4. **City Not Found Errors**
   - Try including country code: "London,GB"
   - Check spelling of city name
   - Some cities may not be available in OpenWeather database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeather](https://openweathermap.org/) for weather data API
- [Chart.js](https://www.chartjs.org/) for beautiful charts
- [Lucide](https://lucide.dev/) for the icon library
- [Vue.js](https://vuejs.org/) team for the amazing framework
- [Flask](https://flask.palletsprojects.com/) for the lightweight backend

## 📞 Support

For support, email [your-email@example.com] or create an issue in the GitHub repository.

---

**⭐ If you found this project helpful, please give it a star!**
