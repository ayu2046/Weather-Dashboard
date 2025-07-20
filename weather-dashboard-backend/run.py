#!/usr/bin/env python3
"""
Weather Dashboard Backend - Flask Application Entry Point

This module serves as the entry point for the Flask application.
It creates and runs the Flask app with development settings enabled.
"""

import os
from app import create_app
from config import get_config

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Get configuration
    config = get_config()
    debug_mode = config.DEBUG
    host = config.HOST
    port = config.PORT
    
    print("=" * 60)
    print("🌤️  Weather Dashboard Backend Starting...")
    print("=" * 60)
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug Mode: {debug_mode}")
    print(f"🔄 Hot Reload: {debug_mode}")
    print("=" * 60)
    print("Available Endpoints:")
    print("  🌡️  GET /api/weather?city=<city_name>")
    print("  📊 GET /api/forecast?city=<city_name>&days=<1-5>")
    print("  🚨 GET /api/alerts?city=<city_name>")
    print("  ❤️  GET /api/health")
    print("=" * 60)
    
    # Check if API key is configured
    if not app.config.get('OPENWEATHER_API_KEY') or app.config.get('OPENWEATHER_API_KEY') == 'your_openweather_api_key_here':
        print("⚠️  WARNING: OpenWeather API key not configured!")
        print("   Please set OPENWEATHER_API_KEY in your .env file")
        print("   Get your free API key from: https://openweathermap.org/api")
        print("=" * 60)
    
    try:
        # Run the Flask development server
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            use_reloader=debug_mode,  # Enable hot reload in debug mode
            use_debugger=debug_mode,  # Enable debugger in debug mode
            threaded=True  # Handle multiple requests concurrently
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Weather Dashboard Backend Stopped")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("=" * 60)
