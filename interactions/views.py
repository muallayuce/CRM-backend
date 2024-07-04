from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Interaction
from .serializers import InteractionSerializer
from rest_framework.permissions import IsAuthenticated

class InteractionListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter('user', OpenApiTypes.STR, description='Filter by user ID'),
            OpenApiParameter('interact_with', OpenApiTypes.STR, description='Filter by interact_with ID'),
            OpenApiParameter('contact', OpenApiTypes.STR, description='Filter by contact ID')
        ],
        responses={200: InteractionSerializer(many=True)},
        description="Retrieve a list of interactions or create a new interaction."
    )
    def get(self, request):
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
        
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=InteractionSerializer,
        responses={201: InteractionSerializer},
        description="Create a new interaction."
    )
    def post(self, request):
        serializer = InteractionSerializer(data=request.data)
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
        request=InteractionSerializer,
        responses={200: InteractionSerializer},
        description="Update a specific interaction."
    )
    def put(self, request, pk):
        interaction = self.get_object(pk)
        serializer = InteractionSerializer(interaction, data=request.data)
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