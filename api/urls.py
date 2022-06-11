from django.urls import include, path

from rest_framework import routers


from api.customAuthToken import CustomAuthToken
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'sondage', views.SondageViewSet)
router.register(r'question', views.QuestionViewSet)
#router.register(r'answer', views.AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
