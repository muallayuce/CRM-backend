from rest_framework import generics
from .models import Won
from .serializers import WonSerializer
from rest_framework.permissions import IsAuthenticated

class WonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Won.objects.all()
    serializer_class = WonSerializer
    permission_classes = [IsAuthenticated]

class WonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Won.objects.all()
    serializer_class = WonSerializer
    permission_classes = [IsAuthenticated]
