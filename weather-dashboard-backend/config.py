"""
Weather Dashboard Backend - Configuration Management

This module centralizes all configuration settings for the Flask application,
including API keys, base URLs, and environment-specific settings.

The configuration is loaded from environment variables using python-dotenv,
with sensible defaults and validation.
"""

import os
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with common settings."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
    TESTING = False
    
    # Server Configuration
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 5000))
    
    # OpenWeather API Configuration
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    OPENWEATHER_BASE_URL = os.environ.get('OPENWEATHER_BASE_URL', 'https://api.openweathermap.org/data/2.5')
    OPENWEATHER_GEOCODING_URL = os.environ.get('OPENWEATHER_GEOCODING_URL', 'http://api.openweathermap.org/geo/1.0/direct')
    OPENWEATHER_ONECALL_URL = os.environ.get('OPENWEATHER_ONECALL_URL', 'https://api.openweathermap.org/data/3.0/onecall')
    
    # API Request Configuration
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 10))
    DEFAULT_UNITS = os.environ.get('DEFAULT_UNITS', 'metric')  # metric, imperial, kelvin
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Rate Limiting (if needed in the future)
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 100))
    
    # Cache Configuration (for future enhancement)
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 300))  # 5 minutes default
    
    @classmethod
    def validate_config(cls) -> list[str]:
        """
        Validate configuration settings and return list of errors.
        
        Returns:
            list[str]: List of validation error messages
        """
        errors = []
        
        # Check required API key
        if not cls.OPENWEATHER_API_KEY:
            errors.append("OPENWEATHER_API_KEY is required but not set")
        elif cls.OPENWEATHER_API_KEY == 'your_openweather_api_key_here':
            errors.append("OPENWEATHER_API_KEY is still set to the default placeholder value")
        elif len(cls.OPENWEATHER_API_KEY) != 32:
            errors.append("OPENWEATHER_API_KEY appears to be invalid (should be 32 characters)")
        
        # Validate units
        if cls.DEFAULT_UNITS not in ('metric', 'imperial', 'kelvin'):
            errors.append("DEFAULT_UNITS must be 'metric', 'imperial', or 'kelvin'")
        
        # Validate timeout
        if cls.API_TIMEOUT <= 0:
            errors.append("API_TIMEOUT must be a positive integer")
        
        # Validate port
        if cls.PORT <= 0 or cls.PORT > 65535:
            errors.append("PORT must be between 1 and 65535")
        
        return errors
    
    @classmethod
    def get_openweather_urls(cls) -> dict[str, str]:
        """
        Get all OpenWeather API URLs.
        
        Returns:
            dict[str, str]: Dictionary of API endpoint URLs
        """
        return {
            'base': cls.OPENWEATHER_BASE_URL,
            'geocoding': cls.OPENWEATHER_GEOCODING_URL,
            'onecall': cls.OPENWEATHER_ONECALL_URL,
            'weather': f"{cls.OPENWEATHER_BASE_URL}/weather",
            'forecast': f"{cls.OPENWEATHER_BASE_URL}/forecast",
        }
    
    @classmethod
    def get_api_params_template(cls) -> dict[str, str]:
        """
        Get template for API request parameters.
        
        Returns:
            dict[str, str]: Common API parameters
        """
        return {
            'appid': cls.OPENWEATHER_API_KEY,
            'units': cls.DEFAULT_UNITS,
        }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    
    # Override defaults for production
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8080))
    
    # More restrictive CORS in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,https://yourdomain.com')


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    
    # Use a test API key if available
    OPENWEATHER_API_KEY = os.environ.get('TEST_OPENWEATHER_API_KEY') or Config.OPENWEATHER_API_KEY


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration class based on environment.
    
    Args:
        env (Optional[str]): Environment name ('development', 'production', 'testing')
                           If None, uses FLASK_ENV environment variable or 'default'
    
    Returns:
        Config: Configuration class instance
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(env, DevelopmentConfig)


# Convenience function to get current configuration
def current_config() -> Config:
    """Get the current configuration based on FLASK_ENV."""
    return get_config()
