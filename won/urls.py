from django.urls import path
from .views import WonListCreateAPIView, WonRetrieveUpdateDestroyAPIView

app_name = "won"

urlpatterns = [
    path('', WonListCreateAPIView.as_view(), name='won-list-create'),
    path('<int:pk>/', WonRetrieveUpdateDestroyAPIView.as_view(), name='won-detail'),
]