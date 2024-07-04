from django.urls import path
from .views import InteractionListCreateAPIView, InteractionDetailAPIView

app_name = "Interactions"

urlpatterns = [
    path('', InteractionListCreateAPIView.as_view(), name='interaction-list-create'),
    path('<int:pk>/', InteractionDetailAPIView.as_view(), name='interaction-detail'),
]