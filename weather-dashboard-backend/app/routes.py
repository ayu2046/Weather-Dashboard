from flask import Blueprint, request, jsonify
from app.services import WeatherService

# Create blueprint
weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather', methods=['GET'])
def get_current_weather():
    """
    Get current weather for a specific city.
    
    Query Parameters:
        city (str): City name (required)
        
    Returns:
        JSON response with weather data or error message
    """
    try:
        city = request.args.get('city')
        
        if not city:
            return jsonify({
                'error': 'City parameter is required',
                'status': 'error'
            }), 400
        
        # Get weather data from service
        weather_data = WeatherService.get_current_weather(city.strip())
        
        if weather_data['status'] == 'error':
            return jsonify(weather_data), 400
        
        return jsonify(weather_data), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@weather_bp.route('/api/forecast', methods=['GET'])
def get_weather_forecast():
    """
    Get weather forecast for a specific city.
    
    Query Parameters:
        city (str): City name (required)
        days (int): Number of days for forecast (optional, default: 5, max: 5)
        
    Returns:
        JSON response with forecast data or error message
    """
    try:
        city = request.args.get('city')
        days = request.args.get('days', 5, type=int)
        
        if not city:
            return jsonify({
                'error': 'City parameter is required',
                'status': 'error'
            }), 400
        
        # Validate days parameter
        if days < 1 or days > 5:
            return jsonify({
                'error': 'Days parameter must be between 1 and 5',
                'status': 'error'
            }), 400
        
        # Get forecast data from service
        forecast_data = WeatherService.get_forecast(city.strip(), days)
        
        if forecast_data['status'] == 'error':
            return jsonify(forecast_data), 400
        
        return jsonify(forecast_data), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@weather_bp.route('/api/alerts', methods=['GET'])
def get_weather_alerts():
    """
    Get weather alerts for a specific city.
    
    Query Parameters:
        city (str): City name (required)
        
    Returns:
        JSON response with alerts data or error message
    """
    try:
        city = request.args.get('city')
        
        if not city:
            return jsonify({
                'error': 'City parameter is required',
                'status': 'error'
            }), 400
        
        # Get alerts data from service
        alerts_data = WeatherService.get_weather_alerts(city.strip())
        
        if alerts_data['status'] == 'error':
            return jsonify(alerts_data), 400
        
        return jsonify(alerts_data), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@weather_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating the API is running
    """
    return jsonify({
        'status': 'success',
        'message': 'Weather Dashboard API is running',
        'version': '1.0.0'
    }), 200

# Error handlers
@weather_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@weather_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error'
    }), 405

@weather_bp.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500
