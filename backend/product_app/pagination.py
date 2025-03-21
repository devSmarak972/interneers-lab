from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    """
    Handles pagination for product listings.
    """
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100