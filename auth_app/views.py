from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from .serializers import LoginSerializer, RegisterSerializer, ChangePasswordSerializer, ChangePasswordByIdSerializer
from drf_spectacular.utils import extend_schema
import logging
from invitation.models import Invitation


logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(APIView):
    """
    User signup view
    """
    @extend_schema(
        description="User signup",
        request=RegisterSerializer
    )
    def post(self, request):
        # Log the start of the method
        logger.debug('Registration request received with data: %s', request.data)

        # Check if any user exists in the database
        if User.objects.exists():
            error_message = "Registration is disabled as there is already a registered user."
            logger.error(error_message)
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
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
        request=LoginSerializer
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

class ChangePasswordView(APIView):
    """
    Change password view
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Change password",
        request=ChangePasswordSerializer
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            print(f"Authenticated user: {user}")  # Log to verify authenticated user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Important to keep the user authenticated
            return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordByIdView(APIView):
    """
    Change password view by admin
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Change password for a user by admin",
        request=ChangePasswordByIdSerializer
    )
    def post(self, request, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

        serializer = ChangePasswordByIdSerializer(data=request.data, context={'request': request, 'user': user})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)