import json
from amqp import NotFound
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

#from common.external_auth import CustomDualAuthentication
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Profile
from teams import swagger_params1
from teams.models import Teams
from teams.serializer import TeamCreateSerializer, TeamsSerializer,TeamswaggerCreateSerializer
from teams.tasks import remove_users, update_team_users


class TeamsListView(APIView, LimitOffsetPagination):
    model = Teams
    #authentication_classes = (CustomDualAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, **kwargs):
        params = self.request.query_params
        queryset = self.model.objects.filter(org=self.request.profile.org).order_by("-id")
        if params:
            if params.get("team_name"):
                queryset = queryset.filter(name__icontains=params.get("team_name"))
            if params.get("created_by"):
                queryset = queryset.filter(created_by=params.get("created_by"))
            if params.get("assigned_users"):
                queryset = queryset.filter(
                    users__id__in=params.get("assigned_users")
                )

        context = {}
        results_teams = self.paginate_queryset(
            queryset.distinct(), self.request, view=self
        )
        teams = TeamsSerializer(results_teams, many=True).data
        if results_teams:
            offset = queryset.filter(id__gte=results_teams[-1].id).count()
            if offset == queryset.count():
                offset = None
        else:
            offset = 0
        context["per_page"] = 10
        page_number = (int(self.offset / 10) + 1,)
        context["page_number"] = page_number
        context.update({"teams_count": self.count, "offset": offset})
        context["teams"] = teams
        return context

    @extend_schema(
        tags=["Teams"], parameters=swagger_params1.teams_list_get_params
    )
    def get(self, *args, **kwargs):
        
        context = self.get_context_data(**kwargs)
        return Response(context)

    @extend_schema(
        tags=["Teams"], request=TeamswaggerCreateSerializer,parameters=swagger_params1.organization_params
    )
    def post(self, request, *args, **kwargs):
        
        serializer = TeamCreateSerializer(data=request.data, request_obj=self.request)
        if serializer.is_valid():
            team_obj = serializer.save()
            return Response(
                {"error": False, "message": "Team Created Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TeamsDetailView(APIView):
    model = Teams
    #authentication_classes = (CustomDualAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk, org=self.request.profile.org)

    @extend_schema(
        tags=["Teams"], parameters=swagger_params1.organization_params
    )
    def get(self, request, pk, **kwargs):
        
        self.team_obj = self.get_object(pk)
        context = {}
        context["team"] = TeamsSerializer(self.team_obj).data
        return Response(context)

    @extend_schema(
        tags=["Teams"], request=TeamswaggerCreateSerializer,parameters=swagger_params1.organization_params
    )
    def put(self, request, pk, *args, **kwargs):
        
        params = request.data
        self.team = self.get_object(pk)
        actual_users = self.team.get_users()
        removed_users = []
        serializer = TeamCreateSerializer(
            data=params, instance=self.team, request_obj=request
        )
        if serializer.is_valid():
            team_obj = serializer.save()

            team_obj.users.clear()
            if params.get("assign_users"):
                assinged_to_list = params.get("assign_users")
                profiles = Profile.objects.filter(
                    id__in=assinged_to_list, org=request.profile.org
                )
                if profiles:
                    team_obj.users.add(*profiles)
            update_team_users.delay(pk)
            latest_users = team_obj.get_users()
            for user in actual_users:
                if user not in latest_users:
                    removed_users.append(user)
            remove_users.delay(removed_users, pk)
            return Response(
                {"error": False, "message": "Team Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        tags=["Teams"], parameters=swagger_params1.organization_params
    )
    def delete(self, request, pk, **kwargs):
        
        self.team_obj = self.get_object(pk)
        self.team_obj.delete()
        return Response(
            {"error": False, "message": "Team Deleted Successfully"},
            status=status.HTTP_200_OK,
        )
    
class TeamsRemoveUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_team_object(self, pk):
        """
        Helper method to retrieve the team object based on the team ID (pk).
        """
        try:
            return Teams.objects.get(pk=pk, org=self.request.profile.org)
        except Teams.DoesNotExist:
            raise NotFound({"error": True, "message": "Team not found."})
    def get_user_object(self, profile_id):
        """
        Helper method to retrieve the user object based on the profile ID.
        """
        try:
            return Profile.objects.get(id=profile_id, org=self.request.profile.org)
        except Profile.DoesNotExist:
            raise NotFound({"error": True, "message": "User not found."})

    @extend_schema(
        tags=["Teams"], parameters=swagger_params1.organization_params
    )
    def delete(self, request, pk, profile_id, **kwargs):
        """Remove a user from a specific team."""
        # Retrieve the team object using the provided team ID (pk)
        team = self.get_team_object(pk)

        # If user_id is not provided, return a 400 Bad Request
        if not profile_id:
            return Response(
                {"error": True, "message": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to get the Profile object of the user
        try:
            user = Profile.objects.get(id=profile_id, org=request.profile.org)
        except Profile.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the user is part of the team
        if user in team.users.all():
            team.users.remove(user)
            return Response(
                {"error": False, "message": "User removed from team successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": True, "message": "User not in this team."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    @extend_schema(
        tags=["Teams"], parameters=swagger_params1.organization_params
    )
    def post(self, request, pk, profile_id, **kwargs):
        """Add a user to a specific team."""
        team = self.get_team_object(pk)
        

        if not profile_id:
            return Response(
                {"error": True, "message": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = Profile.objects.get(id=profile_id, org=request.profile.org)

        if user in team.users.all():
            return Response(
                {"error": True, "message": "User already in this team."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        team.users.add(user)
        return Response(
            {"error": False, "message": "User added to team successfully."},
            status=status.HTTP_200_OK,
        )
