import logging
from datetime import datetime
from django.conf import settings
import os

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

