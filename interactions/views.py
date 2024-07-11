from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Interaction
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from contacts.models import Contact
from common.models import Profile
from leads.models import Lead
from rest_framework.pagination import LimitOffsetPagination


class InteractionListCreateAPIView(APIView, LimitOffsetPagination):
    permission_classes = (IsAuthenticated,)
    model = Interaction

    def get_context_data(self, **kwargs):
        params = self.request.query_params
        queryset = (
            Interaction.objects
            .order_by("-id")
        )

        if params:
            if params.get("name"):
                queryset = queryset.filter(
                    Q(first_name__icontains=params.get("name")) | Q(last_name__icontains=params.get("name"))
                )

        context = {}
        results_interactions = self.paginate_queryset(queryset.distinct(), self.request, view=self)
        interactions = InteractionSerializer(results_interactions, many=True).data
        context["per_page"] = 10
        context["page_number"] = int(self.offset / 10) + 1 if self.offset else 1
        context["interactions"] = {
            "interactions_count": self.count,
            "interactions": interactions,
            "offset": self.offset if self.offset else 0,
        }

        contacts = Contact.objects.filter(org=self.request.profile.org).values("id", "first_name", "last_name")
        context["contacts"] = contacts
        users = Profile.objects.filter(is_active=True, org=self.request.profile.org).values("id", "user__email")
        context["users"] = users
        leads = Lead.objects.filter(org=self.request.profile.org).values("id", "account_name")
        context["leads"] = leads

        return context

    @extend_schema(
        parameters=[
            OpenApiParameter('user', OpenApiTypes.STR, description='Filter by user ID'),
            OpenApiParameter('interact_with', OpenApiTypes.STR, description='Filter by interact_with ID'),
            OpenApiParameter('contact', OpenApiTypes.STR, description='Filter by contact ID')
        ],
        #responses={200: InteractionSerializer(many=True)},
        description="Retrieve a list of interactions or create a new interaction."
    )
    def get(self, request, **kwargs):
        user_id = request.query_params.get('user')
        interact_with_id = request.query_params.get('interact_with')
        contact_id = request.query_params.get('contact')
        
        interactions = Interaction.objects.all()
        
        if user_id:
            interactions = interactions.filter(user_id=user_id)
        if interact_with_id:
            interactions = interactions.filter(interact_with_id=interact_with_id)
        if contact_id:
            interactions = interactions.filter(contact_id=contact_id)
        
        #serializer = InteractionSerializer(interactions, many=True)
        context = self.get_context_data(**kwargs)
        return Response(context)

    @extend_schema(
        request=InteractionCreateSerializer,
        responses={201: InteractionCreateSerializer},
        description="Create a new interaction."
    )
    def post(self, request):
        serializer = InteractionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InteractionDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    @extend_schema(
        responses={200: InteractionSerializer},
        description="Retrieve, update, or delete a specific interaction."
    )
    def get_object(self, pk):
        try:
            return Interaction.objects.get(pk=pk)
        except Interaction.DoesNotExist:
            raise NotFound()
        
    @extend_schema(
        responses={200: InteractionSerializer},
        description="Retrieve a specific interaction."
    )

    def get(self, request, pk):
        interaction = self.get_object(pk)
        serializer = InteractionSerializer(interaction)
        return Response(serializer.data)

    @extend_schema(
        request=InteractionCreateSerializer,
        responses={200: InteractionCreateSerializer},
        description="Update a specific interaction."
    )
    def put(self, request, pk):
        interaction = self.get_object(pk)
        serializer = InteractionCreateSerializer(interaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None},
        description="Delete a specific interaction."
    )
    def delete(self, request, pk):
        interaction = self.get_object(pk)
        interaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)