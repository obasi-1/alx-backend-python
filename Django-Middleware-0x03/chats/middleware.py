import logging
from datetime import datetime
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

