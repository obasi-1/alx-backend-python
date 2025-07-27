import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden, HttpResponseTooManyRequests

# Configure the logger
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(18, 0)  # 6 PM
        end_time = time(21, 0)    # 9 PM

        # Only apply restriction to /chats/ paths
        if request.path.startswith('/chats/'):
            if not (start_time <= current_time <= end_time):
                return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = {}

    def __call__(self, request):
        if request.path.startswith('/chats/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up old requests (older than 1 min)
            if ip not in self.ip_tracker:
                self.ip_tracker[ip] = []
            self.ip_tracker[ip] = [
                timestamp for timestamp in self.ip_tracker[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            if len(self.ip_tracker[ip]) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded. Max 5 messages per minute.")

            self.ip_tracker[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """ Get client IP address from request headers """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that require elevated permissions
        protected_paths = [
            '/chats/admin-actions/',  # Example protected path
        ]

        if any(request.path.startswith(path) for path in protected_paths):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Check if the user has an allowed role
            if getattr(user, 'role', None) not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)
