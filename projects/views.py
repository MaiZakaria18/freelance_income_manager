from django.db import IntegrityError
from rest_framework import  filters, viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsAdminOnly
from .filters import ProjectFilter
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Project
from django.core.paginator import Paginator
from .serializers import ProjectSerializer
from utils.permissions import IsAdminOrOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"project_name": "You already have a project with this name."})

class ProjectSearchView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrOwner]

    def post(self, request, *args, **kwargs):
        pagination_data = request.data.get("pagination", {})
        filter_data = request.data.get("filter", {})

        # Pagination defaults
        page_number = pagination_data.get("page", 1)
        page_size = pagination_data.get("page_size", 10)

        search = filter_data.get("search")
        status_filter = filter_data.get("status")
        ordering = filter_data.get("ordering")

        # Base queryset
        qs = Project.objects.all()
        if request.user.role != 'admin':
            qs = qs.filter(user=request.user)

        # Apply search
        if search:
            qs = qs.filter(
                Q(client_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        # Apply status filter
        if status_filter:
            allowed_statuses = [choice[0] for choice in Project.STATUS_CHOICES]
            if status_filter not in allowed_statuses:
                return Response(
                    {"status": f"Invalid value '{status_filter}', choose from {allowed_statuses}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            qs = qs.filter(status=status_filter)

        # Apply ordering
        if ordering:
            qs = qs.order_by(ordering)

        # Manual pagination
        paginator = Paginator(qs, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.get_serializer(page_obj, many=True)

        return Response({
            "pagination": {
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "page_size": page_size
            },
            "results": serializer.data
        })

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

class AdminProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['client_name', 'user__email']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']