from django.db.models import Avg, Q
from django.core.paginator import Paginator
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Tip
from .serializers import TipSerializer, TipRatingSerializer

class TipListView(generics.GenericAPIView):
    serializer_class = TipSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        pagination_data = request.data.get("pagination", {})
        page_number = pagination_data.get("current_page", 1)
        page_size = pagination_data.get("page_size", 10)

        filter_data = request.data.get("filter", {})
        search = filter_data.get("search")
        category_id = filter_data.get("category")

        tips_qs = Tip.objects.all().select_related("category", "user").annotate(
            avg_rating=Avg("ratings__value")
        )

        if category_id:
            tips_qs = tips_qs.filter(category_id=category_id)

        if search:
            tips_qs = tips_qs.filter(
                Q(text__icontains=search) | Q(category__name__icontains=search)
            )

        tips_qs = tips_qs.order_by("-avg_rating", "-created_at")

        paginator = Paginator(tips_qs, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = self.get_serializer(page_obj, many=True)

        return Response({
            "pagination": {
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "page_size": page_size
            },
            "tips": serializer.data
        })

class TipCreateView(generics.CreateAPIView):
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TipDetailView(generics.RetrieveAPIView):
    queryset = Tip.objects.all().select_related('category', 'user')
    serializer_class = TipSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class TipUpdateView(generics.UpdateAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update your own tips.")
        serializer.save()

class TipDeleteView(generics.DestroyAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own tips.")
        instance.delete()

class TipRatingCreateView(generics.CreateAPIView):
    serializer_class = TipRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
