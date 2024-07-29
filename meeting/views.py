from rest_framework import generics
from .models import Meeting
from .serializers import MeetingSerializer
from rest_framework.permissions import IsAuthenticated

class MeetingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

class MeetingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
