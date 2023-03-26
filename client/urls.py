from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('sondage/<str:slug>', views.sondage),
    path('sondage_content/', views.sondage_data),
]
