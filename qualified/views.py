from rest_framework import generics
from .models import Qualified
from .serializers import QualifiedSerializer
from rest_framework.permissions import IsAuthenticated

class QualifiedListCreateAPIView(generics.ListCreateAPIView):
    queryset = Qualified.objects.all()
    serializer_class = QualifiedSerializer
    permission_classes = [IsAuthenticated]

class QualifiedRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Qualified.objects.all()
    serializer_class = QualifiedSerializer
    permission_classes = [IsAuthenticated]
