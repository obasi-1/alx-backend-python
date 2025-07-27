# Django-Middleware-0x03/chats/middleware.py

from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware to check user roles (admin or moderator) for specific actions.
    If the user does not have the required role, it returns a 403 Forbidden response.
    """
    def __init__(self, get_response):
        """
        Initializes the middleware.
        get_response: The next middleware or the view function.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes the incoming request.
        Checks if the user's role is 'admin' or 'moderator'.
        If not, it returns an HttpResponseForbidden.
        """
        # IMPORTANT: This is a placeholder for how you might determine a user's role.
        # In a real application, you would typically get the role from:
        # - request.user.is_staff or request.user.is_superuser (for Django's built-in User model)
        # - A custom 'role' field on your User model or a related profile model
        # - A session variable or JWT token if using custom authentication.

        # For demonstration purposes, let's assume the role is stored in a session
        # or can be derived from the user object.
        # Replace this logic with how your application actually stores user roles.

        # Example: Assuming you have a custom 'role' attribute on the user object
        # or you've set it in the session during login.
        user_role = getattr(request.user, 'role', 'guest') # Default to 'guest' if no role found

        # Example: If you're using Django's built-in User model and want to check staff/superuser status
        # if request.user.is_authenticated:
        #     if request.user.is_superuser or request.user.is_staff:
        #         user_role = 'admin' # Or 'moderator' based on your specific logic
        #     else:
        #         user_role = 'user'
        # else:
        #     user_role = 'anonymous'


        # Define the roles that are allowed to proceed
        allowed_roles = ['admin', 'moderator']

        # Check if the user is authenticated and has an allowed role
        # You might want to add more specific URL path checks here
        # For example, only apply this middleware to '/admin/' paths or specific API endpoints.
        # if not request.user.is_authenticated or user_role not in allowed_roles:
        #     # This simple check applies to ALL requests. You might want to refine this.
        #     # For instance, only apply to specific URLs or views.
        #     if request.path.startswith('/chats/'): # Example: Only protect /chats/ URLs
        #         if user_role not in allowed_roles:
        #             return HttpResponseForbidden("You do not have permission to access this resource.")

        # A more generic check applying to all requests where this middleware is active
        # Make sure to adjust `user_role` retrieval based on your actual user model/auth system.
        if user_role not in allowed_roles:
            # You can customize the forbidden message
            return HttpResponseForbidden("You do not have the necessary permissions to perform this action.")

        # If the user has an allowed role, or if the middleware doesn't block them,
        # proceed to the next middleware or the view.
        response = self.get_response(request)
        return response

