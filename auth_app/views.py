from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """
    User signup view
    """
    @extend_schema(
        description="User signup",
        request=RegisterSerializer,
        responses={
            201: {
                "description": "Successful signup",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"},
                                "user_id": {"type": "integer"}
                            },
                            "required": ["email", "user_id"]
                        }
                    }
                }
            },
            400: {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "detail": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    )
    def post(self, request):
        # Log the start of the method
        logger.debug('Registration request received with data: %s', request.data)
        
        # Create a serializer instance
        serializer = RegisterSerializer(data=request.data)
        
        # Check if serializer is valid
        if serializer.is_valid():
            # Save the user
            user = serializer.save()
            response = {
                "email": user.email,
                "user_id": user.id
            }
            logger.info('User registered successfully: %s', user.email)
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            # Log invalid data
            logger.error('Invalid data during registration: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class LoginView(APIView):
    """
    User login view
    post:
        Returns token of logged In user
    """

    @extend_schema(
        description="User login",
        request=LoginSerializer,
        responses={
            200: {
                "description": "Successful login",
                "examples": {
                    "application/json": {
                        "username": "user@example.com",
                        "access_token": "some_access_token",
                        "refresh_token": "some_refresh_token",
                        "user_id": 1,
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "examples": {
                    "application/json": {
                        "detail": "Invalid credentials"
                    }
                }
            }
        }
    )
    def post(self, request):
        logger.debug('Login request received with data: %s', request.data)
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Invalid data: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if not user:
            logger.warning('Invalid credentials for email: %s', email)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = RefreshToken.for_user(user)
        response = {
            "username": user.email,
            "access_token": str(token.access_token),
            "refresh_token": str(token),
            "user_id": user.id
        }
        logger.debug('Login successful for user: %s', user.email)
        return Response(response, status=status.HTTP_200_OK)