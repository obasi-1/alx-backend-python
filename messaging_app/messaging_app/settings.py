# settings.py
# Add 'django_filters' to your INSTALLED_APPS
# Make sure 'rest_framework' is also installed if you are using DRF
# pip install djangorestframework django-filter

INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'django_filters',
    'your_app_name', # Replace with the actual name of your Django app
]

# Optional: Configure REST Framework pagination style globally
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20, # Default page size for all paginated views
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
