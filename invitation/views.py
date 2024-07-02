from rest_framework.views import APIView
import string
from crm import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from accounts import swagger_params1
from invitation.models import Invitation
from invitation.serialazer import InvitationSerializer, InvitationCreateSerializer, RegisterSerializer, CreateProfileSerializer, InvitationNewSerializer
#from common.serializer import CreateProfileSerializer
from invitation.models import Invitation
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
import secrets
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
import smtplib
#from .tasks import send_email_async

User = get_user_model()

def generate_password(length=12):
    """Generates a secure random password of the specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def create_new_user(request, temp_password):

    password = temp_password
    # Create a serializer instance
    serializer = RegisterSerializer(data={'email': request.data['invitee_email'],
                                          'password': password})
        
    # Check if serializer is valid
    if serializer.is_valid():
        # Save the user
        user = serializer.save()
        user_data = {
            "email": user.email,
            "user_id": user.id,
            "password": user.password
        }
        return user_data
    else:
        error_message = 'Check your user data in serializer'
        return error_message
    
def create_token(user_data):
    email = user_data.get('email')
    if not email:
        raise ValueError('Missing user email in data for token creation.')

    # Authenticate using email (assuming email-based authentication)
    user = User.objects.get(pk=user_data['user_id'])
    if not user:
        return Response({'message': 'no user'})

    # Create refresh token
    refresh = RefreshToken.for_user(user)

    # Return access token (extracted from refresh token)
    return str(refresh.access_token)
    
def create_profile(request, user_id):
    serializer = CreateProfileSerializer(data={
        'role': request.data['role'],
        'user': user_id,
        'org': request.data['org']
    })

    if serializer.is_valid():
        profile = serializer.save()
        profile_data = {
            'user_id': profile.user,
            'role': profile.role,
            'org_id': profile.org
        }
        return profile_data
    else:
        error_message = 'Check your profile data in serializer'
        return error_message
    
def create_invitation(user_id, token, request):
    serializer = InvitationNewSerializer(data={
        'token': token,
        'invitee_id': user_id,
        'inviter_id': request.data['inviter']
    })

    if serializer.is_valid():
        invite = serializer.save()
        invitation_data = {
            'token': invite.token,
            'invitee_id': invite.invitee_id,
            'inviter_id': invite.inviter_id
        }
        return invitation_data
    else:
        error_message = serializer.errors
        return error_message

    
def send_link(email, token, temp_password, request):

    #user = User.objects.get(pk=request.data['inviter'])

    if not all([email, token, temp_password]):
        raise ValueError('Missing required arguments: email, token or temp_password')
    
    #if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    subject = 'Invitation to join our platform'
    from_email=settings.EMAIL_HOST_USER
    body = f"""
    Hi {email},

    You have been invited to join our platform. Please click the link below to complete your registration and set a new password.

    Link: http://localhost:3000/app/set-password/{token}

    Your temporary password is: {temp_password}
    
    Please note that this temporary password will expire in 1 day. You will need to set a new password upon first login.

    We look forward to welcoming you to our community!

    Kind regards,

    The {settings.WAGTAIL_SITE_NAME} Team
    """

    send_mail(subject, body, from_email, [email], fail_silently=False)

    #message = EmailMessage(
    #    subject=subject,
    #    body=body,
    #    from_email= from_email,
    #    to=[email]
    #)
    #message.attach_alternative(body, 'text/html')  # Add HTML version if needed
    #message.send()
    return Response({'message': 'Succesfully sent'})
    #else:
       # return Response({'message': 'Impossible to send it'})

class InvitationView(APIView):

    model1 = Invitation
    model2 = User
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Invitation"], request=InvitationCreateSerializer)
    def post(self, request):
        temp_password = generate_password()
        # Create a new user
        user_data = create_new_user(request, temp_password)

        # Some data from new user
        user_id = user_data['user_id']
        email = user_data['email']

        # Create new token for invitee user
        token = create_token(user_data)

        # Create profile for invitee user
        profile_data = create_profile(request, user_id)

        # Create invitation for invitee user
        invite_data = create_invitation(user_id, token, request)

        # Send email to invitee user
        send_link(email, token, temp_password, request)

        return Response({'message': 'Succesfully'})