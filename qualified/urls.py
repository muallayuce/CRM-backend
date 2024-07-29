from django.urls import path
from .views import QualifiedListCreateAPIView, QualifiedRetrieveUpdateDestroyAPIView

app_name = "qualified"

urlpatterns = [
    path('', QualifiedListCreateAPIView.as_view(), name='qualified-list-create'),
    path('<int:pk>/', QualifiedRetrieveUpdateDestroyAPIView.as_view(), name='qualified-detail'),
]