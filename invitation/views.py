from rest_framework.views import APIView
import string
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from accounts import swagger_params1
from invitation.models import Invitation
from invitation.serialazer import InvitationSerializer, InvitationCreateSerializer, RegisterSerializer
from invitation.models import Invitation
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
import secrets

class InvitationView(APIView):

    model = Invitation
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Invitation"], parameters=swagger_params1.organization_params, request=InvitationSerializer)
    def get(self, request):

        return Response({'message': 'Works'})