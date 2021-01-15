"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from rest_framework import routers, permissions
from rest_framework_jwt.views import obtain_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from user.views import UserViewSet
from tweet.views import TweetViewSet, AdminActionset, LogsViewset

from tweet.models import Tweet

schema_view = get_schema_view(
    openapi.Info(
        title="Twitter RBAC API",
        default_version='v1',
        description="Endpoints for testing the assesment",
        public=True
      ),
   public=True,
   permission_classes=[permissions.AllowAny],
   )

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'actions', AdminActionset)
router.register(r'logs', LogsViewset)

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^token', obtain_jwt_token, name='get_token'),
    url('', include(router.urls))
]
