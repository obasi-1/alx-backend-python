# messaging/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def delete_user(request):
    """
    A view to handle the deletion of the authenticated user's account.
    This view will be called on a POST request.
    """
    if request.method == 'POST':
        # Get the authenticated user
        user = request.user
        # Log the user out before deletion
        logout(request)
        # Delete the user account
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')  # Redirect to a home page or login page after deletion
    
    return render(request, 'messaging/confirm_delete.html') # A template to confirm deletion
