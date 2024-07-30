from django.urls import path
from .views import MeetingListCreateAPIView, MeetingRetrieveUpdateDestroyAPIView

app_name = "meetings"

urlpatterns = [
    path('meetings/', MeetingListCreateAPIView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingRetrieveUpdateDestroyAPIView.as_view(), name='meeting-detail'),
]