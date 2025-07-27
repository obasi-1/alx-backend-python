from django.urls import path
from .views import ConversationListCreateView, ConversationDetailView, MessageListCreateView, MessageDetailView

urlpatterns = [
    # URL for listing all conversations and creating a new one
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    # URL for retrieving, updating, or deleting a specific conversation
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    # URL for listing messages within a specific conversation and creating a new message
    path('conversations/<int:conversation_pk>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    # URL for retrieving, updating, or deleting a specific message within a conversation
    path('conversations/<int:conversation_pk>/messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]

