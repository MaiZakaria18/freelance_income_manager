from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer, CustomTokenObtainSerializer, UserAdminSerializer
from utils.permissions import IsAdminOnly

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'username', 'profession', 'location']
    ordering_fields = ['avg_monthly_income', 'username']
