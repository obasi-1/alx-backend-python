# messaging_app/settings.py

# ... (other Django settings) ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Make sure rest_framework is in your installed apps
    'chats', # Your chats app
    # ... other apps
]

# ... (other middleware, templates, databases, etc.) ...

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication', # If you are using Token authentication
        # Add other authentication classes if needed (e.g., JWT)
    ],
}

# ... (rest of your settings.py) ...

