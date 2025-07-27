import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpResponseForbidden
import os

# --- RequestLoggingMiddleware Configuration ---
# Configure the logger for requests
# This will create a 'requests.log' file in your project's base directory.
# The level is set to INFO, meaning all INFO, WARNING, ERROR, CRITICAL messages will be logged.
log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s', # We'll format the message directly in the middleware
    handlers=[
        logging.FileHandler(log_file_path)
    ]
)

# Get a specific logger instance for our middleware
request_logger = logging.getLogger('request_logger')
# Prevent the log messages from being propagated to the root logger,
# which might print them to the console if not desired.
request_logger.propagate = False


class RequestLoggingMiddleware:
    """
    Middleware to log each user's request, including timestamp, user, and request path.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        get_response is a callable that takes a request and returns a response.
        """
        self.get_response = get_response
        request_logger.info("RequestLoggingMiddleware initialized.")

    def __call__(self, request):
        """
        Code to be executed for each request before the view is called.
        """
        # Get the current user. If the user is authenticated, it will be the User object,
        # otherwise it will be an AnonymousUser object.
        user = request.user
        # Get the request path.
        path = request.path

        # Log the information using the configured logger.
        # We use f-string for clear formatting.
        log_message = f"{datetime.now()} - User: {user} - Path: {path}"
        request_logger.info(log_message)

        # Call the next middleware or the view.
        response = self.get_response(request)

        # Code to be executed for each response after the view is called.
        # (No specific logging needed for response in this objective, but this is where it would go)

        return response


# --- RestrictAccessByTimeMiddleware Implementation ---
class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours of the day.
    Access is allowed only between 6 PM (18:00) and 9 PM (21:00) server time.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization for the middleware.
        """
        self.get_response = get_response
        # Define the allowed time window (inclusive of start, exclusive of end)
        self.allowed_start_hour = 18 # 6 PM
        self.allowed_end_hour = 21   # 9 PM (meaning up to 20:59:59)

    def __call__(self, request):
        """
        Code to be executed for each request to check access time.
        """
        # Get the current server time.
        now = datetime.now()
        current_hour = now.hour

        # Check if the current hour is outside the allowed range.
        # The condition means: if current_hour is BEFORE 6 PM OR current_hour is AT/AFTER 9 PM
        if not (self.allowed_start_hour <= current_hour < self.allowed_end_hour):
            # If outside the allowed time, return a 403 Forbidden response.
            # You can customize the message here.
            return HttpResponseForbidden("Access to the messaging app is restricted outside 6 PM and 9 PM (server time).")

        # If within the allowed time, proceed with the request.
        response = self.get_response(request)
        return response


# --- OffensiveLanguageMiddleware (Rate Limiting) Implementation ---
class OffensiveLanguageMiddleware: # Renamed as per user's instruction, though it's a rate limiter
    """
    Middleware to limit the number of chat messages (POST requests) a user can send
    within a certain time window, based on their IP address.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization for the middleware.
        """
        self.get_response = get_response
        # Dictionary to store request timestamps for each IP address.
        # Format: {'ip_address': [timestamp1, timestamp2, ...]}
        self.requests_by_ip = {}
        self.RATE_LIMIT_MESSAGES = 5  # Max messages allowed
        self.TIME_WINDOW_SECONDS = 60 # Time window in seconds (1 minute)

    def __call__(self, request):
        """
        Code to be executed for each request to enforce rate limiting.
        """
        # Only apply rate limiting to POST requests, which are typically used for sending messages.
        if request.method == 'POST':
            # Get the client's IP address.
            # Use X-Forwarded-For if behind a proxy, otherwise REMOTE_ADDR.
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            now = datetime.now()

            # Initialize list for IP if it's the first request from this IP.
            if ip not in self.requests_by_ip:
                self.requests_by_ip[ip] = []

            # Clean up old timestamps: remove timestamps older than the time window.
            # This ensures only recent requests are counted.
            self.requests_by_ip[ip] = [
                timestamp for timestamp in self.requests_by_ip[ip]
                if now - timestamp < timedelta(seconds=self.TIME_WINDOW_SECONDS)
            ]

            # Check if the number of requests exceeds the limit.
            if len(self.requests_by_ip[ip]) >= self.RATE_LIMIT_MESSAGES:
                # If limit is exceeded, return a 403 Forbidden response.
                return HttpResponseForbidden(
                    f"Too many requests from your IP address ({ip}). "
                    f"Please wait before sending more messages. Limit: {self.RATE_LIMIT_MESSAGES} per {self.TIME_WINDOW_SECONDS} seconds."
                )
            else:
                # If within limit, add the current request's timestamp.
                self.requests_by_ip[ip].append(now)

        # Proceed with the request if it's not a POST request or if it passed the rate limit.
        response = self.get_response(request)
        return response

