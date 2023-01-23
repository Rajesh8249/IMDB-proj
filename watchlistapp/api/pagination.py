from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination



class watchListPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 7
    # last_page_strings = 'end'
    

class watchListLOpagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'


class watchListCurPagination(CursorPagination):
    page_size = 3
    ordering = 'created'
    cursor_query_param = 'record'
