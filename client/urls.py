from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('sondage/<int:id>', views.sondage),
    path('sondage_content/', views.sondage_data),
    path('question/', views.question)
]
