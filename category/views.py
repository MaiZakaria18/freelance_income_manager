from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminOnly, IsAdminOrOwner
from rest_framework import viewsets, filters
from rest_framework import generics
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from .filter import CategoryFilter


class CategorySearchView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        search_term = request.data.get('search', '').strip()

        queryset = self.get_queryset()
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data})

class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryUpdateView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['name', 'user__email']
    ordering_fields = ['name', 'user__id']
    ordering = ['name']