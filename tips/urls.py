from django.urls import path
from .views import TipCreateView, TipListView, TipRatingCreateView,TipDetailView, TipUpdateView, TipDeleteView

urlpatterns = [
    path('tips/create/', TipCreateView.as_view(), name='tip-create'),
    path('tips/list/', TipListView.as_view(), name='tip-list'),
    path('tips/<int:id>/', TipDetailView.as_view(), name='tip-detail'),
    path('tips/<int:id>/update/', TipUpdateView.as_view(), name='tip-update'),
    path('tips/<int:id>/delete/', TipDeleteView.as_view(), name='tip-delete'),
    path('tips/rate/', TipRatingCreateView.as_view(), name='tip-rate'),
]
