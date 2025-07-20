#!/bin/bash

# Weather Dashboard Backend - Render Start Script
echo "🌤️ Starting Weather Dashboard Backend..."

# Set environment variables for production
export FLASK_ENV=production

# Start the application with gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - wsgi:application
