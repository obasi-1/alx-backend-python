# messaging_app/settings.py

# ... (other Django settings) ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters', # Added django_filters to your installed apps
    'chats',
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
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Default pagination settings (can be overridden per ViewSet)
    'DEFAULT_PAGINATION_CLASS': 'chats.pagination.MessagePagination', # Set your custom pagination class as default
    'PAGE_SIZE': 20, # This sets the default page size if DEFAULT_PAGINATION_CLASS is used
    
    # Default filter backends
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# ... (rest of your settings.py) ...

