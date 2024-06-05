from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from accounts import swagger_params1
from invitation.serialazer import InvitationSerializer


class InvitationView(APIView):
    
    #permission_classes = (AllowAny)
    #serializer_class = AccountReadSerializer

    #def get_object(self, pk):
        #return get_object_or_404(Account, id=pk)

    @extend_schema(tags=["Invitation/"], request=InvitationSerializer)
    def post(self, request):
        return Response({'message': 'Invitation created successfully'}, status=201)