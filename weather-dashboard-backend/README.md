# Weather Dashboard Backend

A Flask-based REST API for weather information using the OpenWeather API.

## 📋 Features

- **Current Weather**: Get real-time weather data for any city
- **Weather Forecast**: 5-day weather forecast with 3-hour intervals
- **Weather Alerts**: Weather alerts and warnings (requires premium API key)
- **CORS Enabled**: Frontend-friendly with Cross-Origin Resource Sharing
- **Error Handling**: Comprehensive error handling with JSON responses
- **Hot Reload**: Development server with automatic reloading

## 🚀 Setup

### Prerequisites
- Python 3.7+
- OpenWeather API key (free from [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd weather-dashboard-backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Edit the `.env` file
   - Replace `your_openweather_api_key_here` with your actual API key:
   ```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

The API will be available at `http://127.0.0.1:5000`

## 📡 API Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status and version

### Current Weather
- **GET** `/api/weather?city=<city_name>`
- Returns current weather data for the specified city
- **Parameters:**
  - `city` (required): City name

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "city": "London",
    "country": "GB",
    "temperature": 18.5,
    "feels_like": 17.8,
    "humidity": 65,
    "pressure": 1013,
    "description": "scattered clouds",
    "icon": "03d",
    "wind_speed": 3.2,
    "wind_direction": 240,
    "visibility": 10.0,
    "timestamp": 1642678800
  }
}
```

### Weather Forecast
- **GET** `/api/forecast?city=<city_name>&days=<1-5>`
- Returns weather forecast for the specified city
- **Parameters:**
  - `city` (required): City name
  - `days` (optional): Number of days (1-5, default: 5)

### Weather Alerts
- **GET** `/api/alerts?city=<city_name>`
- Returns weather alerts for the specified city
- **Parameters:**
  - `city` (required): City name
- **Note:** Requires premium OpenWeather API subscription for full functionality

## 🛠️ Development

### Project Structure
```
weather-dashboard-backend/
├── app/
│   ├── __init__.py          # Flask app factory with CORS
│   ├── routes.py            # API endpoints and error handlers
│   └── services.py          # OpenWeather API service layer
├── docs/
│   └── OPENWEATHER_API_SETUP.md  # Detailed API setup guide
├── config.py                # Centralized configuration management
├── .env                     # Environment variables (comprehensive)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Environment Variables
- `OPENWEATHER_API_KEY`: Your OpenWeather API key
- `DEBUG`: Enable/disable debug mode (default: True)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 5000)

### Error Handling
The API returns consistent JSON error responses:
```json
{
  "error": "Error description",
  "status": "error"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters, invalid city, etc.)
- `404`: Endpoint not found
- `405`: Method not allowed
- `500`: Internal server error

## 🔧 Configuration

### Centralized Configuration Management

The application uses a centralized configuration system with environment-based settings:

- **`config.py`**: Central configuration management with validation
- **`.env`**: Environment variables (development)
- **Environment-specific overrides**: Production, testing, development

### Key Configuration Files

1. **`config.py`**: Centralized configuration classes
   - `Config`: Base configuration
   - `DevelopmentConfig`: Development-specific settings
   - `ProductionConfig`: Production-specific settings
   - `TestingConfig`: Testing-specific settings

2. **`.env`**: Environment variables with comprehensive documentation

### Environment Variables

**Required:**
- `OPENWEATHER_API_KEY`: Your OpenWeather API key (32 characters)

**Optional (with defaults):**
- `FLASK_ENV`: Environment (development/production/testing)
- `DEBUG`: Enable/disable debug mode (True/False)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 5000)
- `API_TIMEOUT`: API request timeout in seconds (default: 10)
- `DEFAULT_UNITS`: Temperature units (metric/imperial/kelvin, default: metric)
- `CORS_ORIGINS`: Allowed CORS origins (default: * for development)

### Configuration Validation

The application automatically validates configuration on startup:
- ✅ API key format and presence
- ✅ Port number validity
- ✅ Timeout values
- ✅ Temperature unit values

### Getting Started with OpenWeather API

📖 **See detailed setup guide**: [`docs/OPENWEATHER_API_SETUP.md`](docs/OPENWEATHER_API_SETUP.md)

**Quick setup:**
1. Get free API key from [openweathermap.org](https://openweathermap.org/api)
2. Replace placeholder in `.env` file:
   ```env
   OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
   ```
3. Wait up to 2 hours for API key activation
4. Start the application: `python run.py`

### CORS Configuration

CORS settings can be configured via environment variables:

**Development (allow all origins):**
```env
CORS_ORIGINS=*
```

**Production (restrict origins):**
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### API Rate Limits

OpenWeather API limits for free accounts:
- **60 calls/minute**
- **1,000 calls/day**
- **1,000,000 calls/month**

The application includes built-in configuration for rate limiting and caching (future features).

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Working:**
   - Ensure your API key is valid and activated
   - Check that it's correctly set in the `.env` file
   - Free API keys may have a delay before activation

2. **City Not Found:**
   - Check the city name spelling
   - Try including the country code: "London,GB"

3. **Network Errors:**
   - Check your internet connection
   - Verify OpenWeather API status

4. **Import Errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.7+)

## 📄 License

This project is open source and available under the MIT License.
