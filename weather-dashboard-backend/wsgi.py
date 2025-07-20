#!/usr/bin/env python3
"""
WSGI Entry Point for Weather Dashboard Backend

This module provides the WSGI application entry point for production deployment
on platforms like Render, Heroku, etc.
"""

import os
from app import create_app

# Set environment to production
os.environ.setdefault('FLASK_ENV', 'production')

# Create the Flask application instance
application = create_app()

# For compatibility with different WSGI servers
app = application

if __name__ == "__main__":
    # For debugging purposes
    application.run()
