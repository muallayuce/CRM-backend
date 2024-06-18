
URL = 3 # here should be URL for first password setting

def generate_password(length=12):
    """Generates a secure random password of the specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

User = get_user_model()

class ExpiringRefreshToken(RefreshToken):
    @property
    def expires_in(self):
        return 60*60*2
    
def create_new_user(email):

    password = generate_password()
    # Create a serializer instance
    serializer = RegisterSerializer(data={
        "email": email,
        "password": password
    })
        
    # Check if serializer is valid
    if serializer.is_valid():
        # Save the user
        user = serializer.save()
        response = {
            "email": user.email,
            "user_id": user.id
        }
        return response
    else:
        error_message = 'Check your data in serializer'
        return Response({"detail": error_message})

def generate_invitation_token(invitee_obj):
    token = ExpiringRefreshToken.objects.get_or_create(user=invitee_obj)
    return token

def generate_and_send_link(token, email, password):
    return URL + '?' + token

class InvitationView(APIView):

    # Class for working with invitations without  usingId
    model = Invitation
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Invitation"], request=InvitationSerializer)
    def get(self, request):

        return 1
    
    
    
class InvitationCreateView(APIView):
    model = Invitation
    permission_classes = (AllowAny,)

    # Create invitation
    @extend_schema(tags=["Invitation"], request=InvitationCreateSerializer, responses={
            201: InvitationSerializer,  # Response code for successful creation
        })
    def post(self, request):
        
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_new_user(request.invitee_email)

        # Get user object based on provided Id (authenticated user)
        if request.inviter == User.id:
            inviter_obj = User
        else:
            return Response(
                {'error': 'You can not create an invitations.'},
                status = status.HTTP_403_FORBIDDEN
            )
        
        invitee_id = serializer.validated_data['invitee']
        try:
            invitee = User.objects.get(id=invitee_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invitee with this id not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate token
        token = RefreshToken.for_user()

        # Create invitation object
        invitation = Invitation.objects.create(
            inviter=inviter_obj.id,
            invitee=invitee.id,
            token=str(token.access_token)
        )

        invitation.save()


        return Response(
            {'message': 'Invitation created successfully'},
            status=status.HTTP_201_CREATED
            )


class InvitationIdView(APIView):

    # Class for working with invitations by using Id 
    model = Invitation
    permission_classes = (AllowAny,)


    # Get invitation by Id
    @extend_schema(tags=["Invitation"], request=InvitationSerializer)
    def get(self, request, pk):

        return 2

    
    # Update invitation by Id
    @extend_schema(tags=["Invitation"], request=InvitationSerializer)
    def put(self, request, pk):
        
        return 3

    # Delete invitation by Id
    @extend_schema(tags=["Invitation"])
    def delete(self, pk):

        return 4
    
class InvitationNewView(APIView):
    model = Invitation
    permission_classes = (AllowAny,)

    @extend_schema(tags=['Invite'])
    def get(self):
        return Response({'message': 'Hello'})