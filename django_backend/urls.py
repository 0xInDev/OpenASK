from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from rest_framework import routers

from api import views

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('import/', views.list, name='fileupload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
