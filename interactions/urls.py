from django.urls import path
from .views import InteractionListCreateAPIView, InteractionDetailAPIView

urlpatterns = [
    path('interactions/', InteractionListCreateAPIView.as_view(), name='interaction-list-create'),
    path('interactions/<int:pk>/', InteractionDetailAPIView.as_view(), name='interaction-detail'),
]