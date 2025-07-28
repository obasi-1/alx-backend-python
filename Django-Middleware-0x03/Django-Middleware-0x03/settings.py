# Django-Middleware-0x03/settings.py

# This is a placeholder for your full settings.py file.
# You would typically have many other settings here, such as:
# DEBUG = True
# ALLOWED_HOSTS = []
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'chats', # Make sure your 'chats' app is listed here
# ]
# DATABASES = { ... }
# AUTH_PASSWORD_VALIDATORS = [ ... ]
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True
# STATIC_URL = 'static/'
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- MIDDLEWARE Configuration ---
# This list defines the order in which middleware components are applied to requests.
# Your custom middleware should be placed strategically.
# It typically comes after AuthenticationMiddleware if it relies on user authentication.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]

# ... other settings would continue here ...
