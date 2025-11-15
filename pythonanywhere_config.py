"""
PythonAnywhere Settings Module
Load this in settings.py to use environment-specific configurations
"""

import os
from pathlib import Path

def is_pythonanywhere():
    """Check if running on PythonAnywhere"""
    return 'PYTHONANYWHERE_DOMAIN' in os.environ or os.path.exists('/home/yourusername/.pythonanywhere_secret_key.txt')

def load_pythonanywhere_config():
    """Load PythonAnywhere-specific configuration"""
    
    config = {
        'DEBUG': False,
        'SECURE_BROWSER_XSS_FILTER': True,
        'SESSION_COOKIE_SECURE': True,
        'CSRF_COOKIE_SECURE': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'SECURE_HSTS_SECONDS': 31536000,
        'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
        'SECURE_HSTS_PRELOAD': True,
        'SECURE_SSL_REDIRECT': False,  # Set to True if SSL is enabled
    }
    
    return config

# Example usage in settings.py:
# if is_pythonanywhere():
#     pythonanywhere_config = load_pythonanywhere_config()
#     DEBUG = pythonanywhere_config['DEBUG']
#     SECURE_BROWSER_XSS_FILTER = pythonanywhere_config['SECURE_BROWSER_XSS_FILTER']
#     # ... etc
