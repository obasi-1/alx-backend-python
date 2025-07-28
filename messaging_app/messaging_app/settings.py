# messaging_app/settings.py

import datetime
import os # Import os for secret key management

# ... other existing settings ...

INSTALLED_APPS = [
    # ... your existing apps ...
    'rest_framework',
    'rest_framework_simplejwt',
    'chats', # Ensure your 'chats' app is listed here
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
        'rest_framework.authentication.BasicAuthentication',    
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Default to requiring authentication for all views
    ),
}

# --- JWT Authentication Settings ---
# IMPORTANT: For production, generate a strong, random key and store it securely
# (e.g., in an environment variable) instead of hardcoding it.
# Example: os.environ.get('DJANGO_SECRET_KEY', 'your-insecure-default-key')
# You can generate a good key with: import os; os.urandom(32).hex()
SECRET_KEY_JWT = os.environ.get('DJANGO_JWT_SECRET_KEY', 'your-very-secret-and-long-jwt-key-please-change-this-in-production')


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=5), # How long access tokens are valid
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),  # How long refresh tokens are valid
    'ROTATE_REFRESH_TOKENS': False, # Set to True if you want refresh tokens to rotate
    'BLACKLIST_AFTER_ROTATION': False, # Set to True if you rotate tokens and want old ones blacklisted
    'UPDATE_LAST_LOGIN': False, # Set to True to update user's last login on token refresh

    'ALGORITHM': 'HS256', # Hashing algorithm for tokens
    'SIGNING_KEY': SECRET_KEY_JWT, # Use the secret key defined above
    'VERIFYING_KEY': None, # Not needed if using the same key for signing and verifying
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0, # Time leeway for token expiration (e.g., 5 minutes for clock skew)

    'AUTH_HEADER_TYPES': ('Bearer',), # The type of header used for authentication (e.g., "Bearer <token>")
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION', # The name of the HTTP header
    'USER_ID_FIELD': 'id', # The field in the User model that uniquely identifies the user
    'USER_ID_CLAIM': 'user_id', # The claim in the token that holds the user ID
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type', # The claim in the token that holds the token type (e.g., "access", "refresh")
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti', # JWT ID claim for unique token identification

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

# ... rest of your settings ...
