from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from user.serializers import UserSerializer
from tweet.utils import isSuperAdmin

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all().exclude(is_superuser=True).order_by('-date_joined')
        return User.objects.all().order_by('-date_joined')