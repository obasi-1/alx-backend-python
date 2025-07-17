from django.urls import path, include
from rest_framework import routers
# Import NestedDefaultRouter from drf_nested_routers
from rest_framework_nested import routers as nested_routers

from .views import ConversationViewSet, MessageViewSet

# Create a top-level router for Conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router for Messages under Conversations
# This will generate URLs like /conversations/{conversation_pk}/messages/
conversations_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    # Include the URLs from the top-level router
    path('', include(router.urls)),
    # Include the URLs from the nested router
    path('', include(conversations_router.urls)),
]
