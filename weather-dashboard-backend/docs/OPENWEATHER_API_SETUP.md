# OpenWeather API Setup Guide

This guide walks you through obtaining and configuring your OpenWeather API key for the Weather Dashboard application.

## 📋 Table of Contents

1. [Why OpenWeather API?](#why-openweather-api)
2. [Getting Your Free API Key](#getting-your-free-api-key)
3. [API Key Configuration](#api-key-configuration)
4. [API Plans and Limits](#api-plans-and-limits)
5. [Testing Your Setup](#testing-your-setup)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

## 🌟 Why OpenWeather API?

OpenWeather provides reliable weather data with:
- **Current weather data** for any location worldwide
- **5-day weather forecasts** with 3-hour intervals
- **Weather alerts** and warnings (premium feature)
- **Free tier** with up to 1,000 API calls per day
- **99.9% uptime guarantee**

## 🔑 Getting Your Free API Key

### Step 1: Create an Account

1. Visit [OpenWeatherMap.org](https://openweathermap.org/api)
2. Click on **"Sign Up"** in the top-right corner
3. Fill out the registration form:
   - **Username**: Your desired username
   - **Email**: A valid email address
   - **Password**: A secure password
   - **Confirm Password**: Re-enter your password
   - **Company**: Optional (you can enter "Personal" or leave blank)
   - **Purpose**: Select "Education" or "Other" for personal projects

4. Check the boxes to agree to the Terms of Service and Privacy Policy
5. Click **"Create Account"**
6. Check your email and click the verification link

### Step 2: Get Your API Key

1. After verifying your email, log in to your OpenWeather account
2. Navigate to the [API Keys section](https://home.openweathermap.org/api_keys)
3. You'll see a default API key already generated for you
4. Copy this key (it should be 32 characters long)
5. **Important**: Keep this key secure and never share it publicly!

### Step 3: Wait for Activation (Important!)

⏰ **Your API key may take up to 2 hours to activate after registration.**

If you get authentication errors immediately after signup, wait a bit and try again.

## ⚙️ API Key Configuration

### Method 1: Using the .env File (Recommended)

1. Open the `.env` file in your project root:
   ```bash
   weather-dashboard-backend/.env
   ```

2. Replace the placeholder with your actual API key:
   ```env
   OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
   ```

3. Save the file

### Method 2: Environment Variable

You can also set the API key as a system environment variable:

**Windows:**
```cmd
set OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
```

**macOS/Linux:**
```bash
export OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
```

### Method 3: .env.local (For Local Development)

Create a `.env.local` file in your project root and add:
```env
OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
```

This file should be added to your `.gitignore` to keep your API key secure.

## 📊 API Plans and Limits

### Free Plan (Recommended for Development)
- **1,000 API calls/day**
- **60 calls/minute**
- Current weather data
- 5-day weather forecast
- Basic weather alerts (limited)

### Paid Plans (For Production)
- **Startup**: $40/month, 100,000 calls/day
- **Developer**: $180/month, 300,000 calls/day
- **Professional**: $600/month, 1,000,000 calls/day
- **Enterprise**: Custom pricing

For most development and small production apps, the free plan is sufficient.

## 🧪 Testing Your Setup

### 1. Start the Application

```bash
cd weather-dashboard-backend
python run.py
```

Look for this output:
```
🌤️  Weather Dashboard Backend Starting...
============================================================
📍 Host: 127.0.0.1
🔌 Port: 5000
🐛 Debug Mode: True
🔄 Hot Reload: True
============================================================
```

If you see a warning about the API key, it's not configured correctly.

### 2. Test API Endpoints

Open your browser or use curl to test:

**Current Weather:**
```bash
curl "http://localhost:5000/api/weather?city=London"
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "city": "London",
    "country": "GB",
    "temperature": 15.5,
    "description": "clear sky",
    ...
  }
}
```

**5-Day Forecast:**
```bash
curl "http://localhost:5000/api/forecast?city=London&days=3"
```

### 3. Health Check

```bash
curl "http://localhost:5000/api/health"
```

Expected response:
```json
{
  "status": "success",
  "message": "Weather Dashboard API is running",
  "version": "1.0.0"
}
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "Invalid API key" Error
- **Cause**: API key is incorrect or not activated yet
- **Solution**: 
  - Double-check your API key (should be exactly 32 characters)
  - Wait up to 2 hours for activation if you just registered
  - Regenerate your API key in the OpenWeather dashboard

#### 2. "API key not configured" Error
- **Cause**: Environment variable not set properly
- **Solution**:
  - Check your `.env` file for typos
  - Ensure the line is: `OPENWEATHER_API_KEY=your_key_here` (no spaces around `=`)
  - Restart your application after changing the `.env` file

#### 3. "City not found" Error
- **Cause**: City name is misspelled or not recognized
- **Solution**:
  - Use full city names: "New York" instead of "NY"
  - Try adding country codes: "London,UK" or "Paris,FR"
  - Check OpenWeather's supported locations

#### 4. 429 "Too Many Requests" Error
- **Cause**: You've exceeded the rate limit
- **Solution**:
  - Free plan: 60 calls/minute, 1000 calls/day
  - Implement caching in your application
  - Upgrade to a paid plan if needed

#### 5. Network/Timeout Errors
- **Cause**: Network connectivity issues
- **Solution**:
  - Check your internet connection
  - Try increasing the timeout in `config.py`:
    ```python
    API_TIMEOUT = 30  # Increase from 10 to 30 seconds
    ```

### Debugging Steps

1. **Verify API Key Format:**
   ```bash
   echo $OPENWEATHER_API_KEY | wc -c
   # Should output 33 (32 chars + newline)
   ```

2. **Test API Key Manually:**
   ```bash
   curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
   ```

3. **Check Application Logs:**
   Look for configuration warnings when starting the app.

## 🔐 Advanced Configuration

### Custom API Endpoints

You can customize the OpenWeather API endpoints in your `.env` file:

```env
# Custom API endpoints (usually not needed)
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
OPENWEATHER_GEOCODING_URL=http://api.openweathermap.org/geo/1.0/direct
OPENWEATHER_ONECALL_URL=https://api.openweathermap.org/data/3.0/onecall
```

### Environment-Specific Configuration

For production deployments, create environment-specific settings:

**Production (.env.production):**
```env
OPENWEATHER_API_KEY=your_production_api_key_here
FLASK_ENV=production
DEBUG=False
API_TIMEOUT=30
CORS_ORIGINS=https://yourdomain.com
```

### API Key Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables in production**
3. **Rotate API keys regularly**
4. **Monitor API usage in the OpenWeather dashboard**
5. **Set up alerts for unusual usage patterns**

## 📚 Additional Resources

- [OpenWeather API Documentation](https://openweathermap.org/api)
- [Weather Data API Guide](https://openweathermap.org/guide)
- [API Response Examples](https://openweathermap.org/current)
- [Status Page](https://openweatherstatus.com/)
- [Support](https://openweathermap.org/faq)

## 🆘 Still Need Help?

If you're still having issues:

1. Check the [OpenWeather FAQ](https://openweathermap.org/faq)
2. Review your account status in the [OpenWeather Dashboard](https://home.openweathermap.org/)
3. Create an issue in this project's repository
4. Contact OpenWeather support for API-specific issues

---

**Happy Coding! 🌤️**
