# messaging_app/chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for Message objects.
    Sets the default page size to 20 messages per page.
    Allows clients to specify page size using 'page_size' query parameter,
    with a maximum limit of 100 messages per page.
    """
    page_size = 20  # Default number of messages per page
    page_size_query_param = 'page_size'  # Allows client to set page size (e.g., ?page_size=10)
    max_page_size = 100  # Maximum page size allowed to prevent abuse

