from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware to check the user's role (admin/staff) before allowing access to specific actions.
    This implementation restricts access to the Django admin site (/admin/) for non-staff users.
    For more granular control over specific API actions, you might consider Django REST Framework's
    permission classes directly on your views in addition to or instead of this middleware.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization for the middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request to enforce role-based access.
        """
        # Allow access to static files and the admin login page for all users.
        # This prevents blocking CSS/JS for the admin site and allows users to log in.
        if request.path.startswith(('/static/', '/admin/login/')):
            return self.get_response(request)

        # Check if the request is for an admin path (any path starting with /admin/ except login)
        if request.path.startswith('/admin/'):
            # If the user is not authenticated OR is authenticated but not a staff member,
            # deny access with a 403 Forbidden response.
            # `is_staff` is typically used for users who can access the admin site.
            if not request.user.is_authenticated or not request.user.is_staff:
                return HttpResponseForbidden("You do not have the necessary permissions to access this page. Only administrators can access the admin site.")

        # If the request is not for a restricted path, or if the user has the required permission,
        # proceed to the next middleware or view.
        response = self.get_response(request)
        return response

