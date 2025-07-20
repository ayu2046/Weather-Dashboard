from flask import Flask
from flask_cors import CORS
import os
from config import get_config, Config

def create_app(config_name: str = None) -> Flask:
    """Create and configure the Flask application."""
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Validate configuration
    validation_errors = config_class.validate_config()
    if validation_errors:
        for error in validation_errors:
            app.logger.warning(f"Configuration warning: {error}")
    
    # Configure CORS
    cors_origins = config_class.CORS_ORIGINS
    if cors_origins == '*':
        CORS(app, origins="*")
    else:
        origins_list = [origin.strip() for origin in cors_origins.split(',')]
        CORS(app, origins=origins_list)
    
    # Store config class in app for easy access
    app.config['CONFIG_CLASS'] = config_class
    
    # Register routes
    from app.routes import weather_bp
    app.register_blueprint(weather_bp)
    
    # Log configuration info
    if not app.config['TESTING']:
        app.logger.info(f"Flask app created with {config_class.__name__}")
        if validation_errors:
            app.logger.warning(f"Found {len(validation_errors)} configuration issues")
    
    return app
