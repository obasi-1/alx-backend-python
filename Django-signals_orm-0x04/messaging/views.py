# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message
from django.http import HttpResponse

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

@login_required
def send_message(request):
    """
    A view to send a new message.
    """
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_message_id = request.POST.get('parent_message_id')
        
        try:
            # Find the receiver user
            receiver_user = get_object_or_404(User, username=receiver_username)
            parent_message = None
            if parent_message_id:
                parent_message = get_object_or_404(Message, pk=parent_message_id)

            # Create the message instance
            Message.objects.create(
                sender=request.user,
                receiver=receiver_user,
                content=content,
                parent_message=parent_message
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('message_list') # Redirect to a message list view
        except User.DoesNotExist:
            messages.error(request, 'Recipient user does not exist.')
            return redirect('send_message')
    
    return render(request, 'messaging/send_message.html', {'users': User.objects.exclude(pk=request.user.pk)})

@login_required
def message_list(request):
    """
    Displays a list of unread messages for the authenticated user,
    using a custom manager for optimized queries.
    """
    messages = Message.unread_messages.for_user(request.user).order_by('-timestamp')
    
    context = {
        'messages': messages,
    }
    return render(request, 'messaging/message_list.html', context)
