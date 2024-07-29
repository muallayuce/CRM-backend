from django.urls import path
from .views import NegotiationListCreateAPIView, NegotiationRetrieveUpdateDestroyAPIView

app_name = "negotiation"

urlpatterns = [
    path('', NegotiationListCreateAPIView.as_view(), name='negotiation-list-create'),
    path('<int:pk>/', NegotiationRetrieveUpdateDestroyAPIView.as_view(), name='negotiation-detail'),
]