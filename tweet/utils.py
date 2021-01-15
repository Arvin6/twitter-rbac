from enum import Enum
from django.contrib.auth.signals import user_logged_in
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

class AdminActions(Enum):
    create = "CREATE"
    delete = "DELETE"
    update = "UPDATE"

class LogActions(Enum):
    create = "CREATE"
    delete = "DELETE"
    update = "UPDATE"
    view   = "VIEW"
    login  = "LOGIN"

class LogTypes(Enum):
    audit = "AUDIT"
    action = "ACTION"
    access = "ACCESS"

class isSuperAdmin(permissions.BasePermission):
    """
    Custom permission class for is_superadmin check
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class adminCanOnlyView(permissions.BasePermission):
    """
    Custom permission class for is_superadmin check
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return request.method == 'GET'
        return True

class CustomListModelMixin:
    """
    Mixin class to enable custom list method 
    with pagination and support for counts
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = request.query_params.get('count', "false").lower() == "true"
        if not count:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # If superadmin wants to query the frequency
            num_results = queryset.count()
            return Response(data={"count": num_results})


def jwt_response_payload_handler(token, user=None, request=None):
    # Custom handler for handling access logs
    if user and request:
        user_logged_in.send(sender=user.__class__, request=request, user=user)
    return {
        'token': token,
    }
