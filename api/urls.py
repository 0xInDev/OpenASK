from django.urls import include, path

from rest_framework import routers


from api.customAuthToken import CustomAuthToken
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'sondage', views.SondageViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'response', views.ResponseViewSet)
router.register(r'response_proposal', views.ResponseProposalViewSet)
router.register(r'question_response', views.QuestionResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
