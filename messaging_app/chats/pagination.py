from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for Message list.
    Sets page size to 20, allows client to specify page size up to 100.
    Overrides get_paginated_response to include total_count in the response.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Returns a paginated API response, including the total count of items.
        """
        return Response({
            'total_count': self.page.paginator.count, # This is where page.paginator.count is used
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
