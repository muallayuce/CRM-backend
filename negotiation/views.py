from rest_framework import generics
from .models import Negotiation
from .serializers import NegotiationSerializer
from rest_framework.permissions import IsAuthenticated

class NegotiationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer
    permission_classes = [IsAuthenticated]

class NegotiationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Negotiation.objects.all()
    serializer_class = NegotiationSerializer
    permission_classes = [IsAuthenticated]