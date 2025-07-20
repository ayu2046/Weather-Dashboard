import requests
from flask import current_app
from typing import Dict, Any, Optional
from config import Config

class WeatherService:
    """Service class for OpenWeather API interactions."""
    
    @staticmethod
    def _get_config() -> Config:
        """Get the current configuration."""
        return current_app.config.get('CONFIG_CLASS', Config)
    
    @staticmethod
    def _get_common_params() -> Dict[str, str]:
        """Get common API parameters."""
        config = WeatherService._get_config()
        return config.get_api_params_template()
    
    @staticmethod
    def get_current_weather(city: str) -> Dict[str, Any]:
        """
        Get current weather for a specific city.
        
        Args:
            city (str): City name
            
        Returns:
            Dict containing weather data or error information
        """
        try:
            config = WeatherService._get_config()
            
            if not config.OPENWEATHER_API_KEY:
                return {
                    'error': 'API key not configured',
                    'status': 'error'
                }
            
            urls = config.get_openweather_urls()
            params = config.get_api_params_template()
            params['q'] = city
            
            response = requests.get(urls['weather'], params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response
            return {
                'status': 'success',
                'data': {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                    'timestamp': data['dt']
                }
            }
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {
                    'error': 'City not found',
                    'status': 'error'
                }
            elif response.status_code == 401:
                return {
                    'error': 'Invalid API key',
                    'status': 'error'
                }
            else:
                return {
                    'error': f'API error: {e}',
                    'status': 'error'
                }
        except requests.exceptions.RequestException as e:
            return {
                'error': f'Network error: {str(e)}',
                'status': 'error'
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {str(e)}',
                'status': 'error'
            }
    
    @staticmethod
    def get_forecast(city: str, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a specific city.
        
        Args:
            city (str): City name
            days (int): Number of days for forecast (default: 5)
            
        Returns:
            Dict containing forecast data or error information
        """
        try:
            config = WeatherService._get_config()
            
            if not config.OPENWEATHER_API_KEY:
                return {
                    'error': 'API key not configured',
                    'status': 'error'
                }
            
            urls = config.get_openweather_urls()
            params = config.get_api_params_template()
            params.update({
                'q': city,
                'cnt': days * 8  # 8 forecasts per day (every 3 hours)
            })
            
            response = requests.get(urls['forecast'], params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the forecast data
            forecasts = []
            for item in data['list']:
                forecasts.append({
                    'datetime': item['dt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind'].get('deg', 0),
                    'pop': item.get('pop', 0) * 100  # Probability of precipitation as percentage
                })
            
            return {
                'status': 'success',
                'data': {
                    'city': data['city']['name'],
                    'country': data['city']['country'],
                    'forecasts': forecasts
                }
            }
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {
                    'error': 'City not found',
                    'status': 'error'
                }
            elif response.status_code == 401:
                return {
                    'error': 'Invalid API key',
                    'status': 'error'
                }
            else:
                return {
                    'error': f'API error: {e}',
                    'status': 'error'
                }
        except requests.exceptions.RequestException as e:
            return {
                'error': f'Network error: {str(e)}',
                'status': 'error'
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {str(e)}',
                'status': 'error'
            }
    
    @staticmethod
    def get_weather_alerts(city: str) -> Dict[str, Any]:
        """
        Get weather alerts for a specific city.
        Note: This requires coordinates, so we'll first get city info then alerts.
        
        Args:
            city (str): City name
            
        Returns:
            Dict containing alerts data or error information
        """
        try:
            config = WeatherService._get_config()
            
            if not config.OPENWEATHER_API_KEY:
                return {
                    'error': 'API key not configured',
                    'status': 'error'
                }
            
            urls = config.get_openweather_urls()
            
            # First, get city coordinates
            geo_params = {
                'q': city,
                'appid': config.OPENWEATHER_API_KEY,
                'limit': 1
            }
            
            geo_response = requests.get(urls['geocoding'], params=geo_params, timeout=config.API_TIMEOUT)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data:
                return {
                    'error': 'City not found',
                    'status': 'error'
                }
            
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            # Now get alerts using One Call API
            alert_params = {
                'lat': lat,
                'lon': lon,
                'appid': config.OPENWEATHER_API_KEY,
                'exclude': 'minutely,hourly,daily,current'  # Only get alerts
            }
            
            alert_response = requests.get(urls['onecall'], params=alert_params, timeout=config.API_TIMEOUT)
            
            # Handle case where alerts API might not be available
            if alert_response.status_code == 401:
                return {
                    'status': 'success',
                    'data': {
                        'city': city,
                        'alerts': [],
                        'message': 'Weather alerts require a premium API subscription'
                    }
                }
            
            alert_response.raise_for_status()
            alert_data = alert_response.json()
            
            alerts = []
            if 'alerts' in alert_data:
                for alert in alert_data['alerts']:
                    alerts.append({
                        'sender_name': alert.get('sender_name', 'Unknown'),
                        'event': alert.get('event', 'Weather Alert'),
                        'start': alert.get('start'),
                        'end': alert.get('end'),
                        'description': alert.get('description', 'No description available')
                    })
            
            return {
                'status': 'success',
                'data': {
                    'city': city,
                    'alerts': alerts
                }
            }
            
        except requests.exceptions.HTTPError as e:
            if alert_response.status_code == 404:
                return {
                    'error': 'Location not found',
                    'status': 'error'
                }
            elif alert_response.status_code == 401:
                return {
                    'status': 'success',
                    'data': {
                        'city': city,
                        'alerts': [],
                        'message': 'Weather alerts require a premium API subscription'
                    }
                }
            else:
                return {
                    'error': f'API error: {e}',
                    'status': 'error'
                }
        except requests.exceptions.RequestException as e:
            return {
                'error': f'Network error: {str(e)}',
                'status': 'error'
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {str(e)}',
                'status': 'error'
            }
