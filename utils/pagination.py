from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if request.method in ["POST", "PUT", "PATCH"]:
            body_pagination = request.data.get("pagination", {})
            page = body_pagination.get("page")
            page_size = body_pagination.get("page_size")

            if page is not None:
                request._request.GET = request._request.GET.copy()
                request._request.GET["page"] = str(page)

            if page_size is not None:
                request._request.GET = request._request.GET.copy()
                request._request.GET["page_size"] = str(page_size)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            "pagination": {
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "total_items": self.page.paginator.count
            },
            "results": data
        })