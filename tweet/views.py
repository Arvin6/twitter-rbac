import logging
import copy

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework import permissions, exceptions
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from tweet.utils import isSuperAdmin, adminCanOnlyView, CustomListModelMixin
from tweet.models import Tweet, RequestAction, Logs
from tweet.serializers import (
                    CreateUpdateDeleteTweetSerializer, 
                    TweetSerializer, RequestActionSerializer, 
                    CreateDeleteRequestActionSerializer,
                    UpdateRequestActionSerializer,
                    LogSerializer,
                )

count_param = openapi.Parameter(
        'count', openapi.IN_QUERY, 
        description="boolean on whether to return count or not", 
        type=openapi.TYPE_BOOLEAN
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(process)d %(thread)d - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, adminCanOnlyView]
    queryset = Tweet.objects.all()
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Tweet.objects.none()
        kwargs = {
            "is_deleted": False,
        }
        current_user = self.request.user
        if not current_user.is_superuser and not current_user.is_staff:
            kwargs['created_by'] = self.request.user
        if current_user.is_superuser:
            kwargs.pop('is_deleted', None)
        return Tweet.objects.filter(**kwargs).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return CreateUpdateDeleteTweetSerializer
        return TweetSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator",
    manual_parameters=[count_param]
))
class AdminActionset(CustomListModelMixin, 
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = RequestAction.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action', 'is_approved', 'created_by', 'updated_by']

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            if self.request.method == 'PATCH':
                return UpdateRequestActionSerializer
            return CreateDeleteRequestActionSerializer
        return RequestActionSerializer

    def update(self, request, **kwargs):
        partial = kwargs['partial']
        if not partial:
            # Only PATCH is allowed
            return self.http_method_not_allowed(request)
        if not request.user.is_superuser:
            raise exceptions.PermissionDenied("Only superadmins can approve requests")
        super().update(request, **kwargs)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator",
    manual_parameters=[count_param]
))
class LogsViewset(CustomListModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [isSuperAdmin]
    queryset = Logs.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'action', 'action_type']

