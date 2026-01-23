"""
Settings package - selects environment based on DJANGO_SETTINGS_MODULE

Usage:
    export DJANGO_SETTINGS_MODULE=online.settings.development   # Linux/Mac
    set DJANGO_SETTINGS_MODULE=online.settings.development      # Windows

Or use the provided run.py script which automatically selects settings.
"""

import os

ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *
