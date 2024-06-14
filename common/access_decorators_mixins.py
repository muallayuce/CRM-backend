from rest_framework import permissions
from common.models import Profile


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Retrieve the profile associated with the user
                profile = request.user.profile
                # Allow GET and POST requests for users with 'ADMIN' role
                if request.method in ['GET', 'POST'] and profile.role == 'ADMIN':
                    return True
                # Deny permission for other methods or non-admin users
                else:
                    return False
            except Profile.DoesNotExist:
                # If the profile does not exist, deny permission
                return False
        # Deny permission if user is not authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has a profile
        if request.user.is_authenticated:
            try:
                # Retrieve the profile associated with the user
                profile = request.user.profile
                # Allow superusers full access to all objects
                if request.user.is_superuser:
                    return True
                # Allow users with 'ADMIN' role access to objects
                elif profile.role == 'ADMIN':
                    return True
                # Default deny for non-admin users
                else:
                    return False
            except Profile.DoesNotExist:
                # If the profile does not exist, deny permission
                return False
        # Deny permission if user is not authenticated
        return False
    
class SalesAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Check if the user's profile has sales access
                if request.user.profile.has_sales_access:
                    # Allow GET and POST requests
                    if request.method in ['GET', 'POST']:
                        return True
                return False
            except Profile.DoesNotExist:
                # If the profile does not exist, deny permission
                return False
        # Deny permission if user is not authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has sales access
        if request.user.is_authenticated:
            try:
                # Check if the user's profile has sales access
                if request.user.profile.has_sales_access:
                    return True
                return False
            except Profile.DoesNotExist:
                return False
        return False
    
class MarketingAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Check if the user's profile has marketing access
                if request.user.profile.has_marketing_access:
                    # Allow GET and POST requests
                    if request.method in ['GET', 'POST']:
                        return True
                return False
            except Profile.DoesNotExist:
                # If the profile does not exist, deny permission
                return False
        # Deny permission if user is not authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has marketing access
        if request.user.is_authenticated:
            try:
                # Check if the user's profile has marketing access
                if request.user.profile.has_marketing_access:
                    return True
                return False
            except Profile.DoesNotExist:
                return False
        return False