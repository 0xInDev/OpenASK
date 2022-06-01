from django.urls import include, path

from rest_framework.authtoken import views as autViews
from rest_framework import routers


from api.customAuthToken import CustomAuthToken
from . import views


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
