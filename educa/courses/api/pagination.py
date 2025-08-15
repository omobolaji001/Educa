from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """ Control how many objects are sent over API responses """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
