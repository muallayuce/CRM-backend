from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    },
    required=['email', 'password']
)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=login_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id})
