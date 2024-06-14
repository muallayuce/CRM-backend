from rest_framework import permissions
from common.models import Profile

class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.role == 'ADMIN':
                    return True
                return False
            except Profile.DoesNotExist:
                return False
        return False

class SalesAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                if request.user.profile.has_sales_access:
                    return True
                return False
            except Profile.DoesNotExist:
                return False
        return False

class MarketingAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                if request.user.profile.has_marketing_access:
                    return True
                return False
            except Profile.DoesNotExist:
                return False
        return False
