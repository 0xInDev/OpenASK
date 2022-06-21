from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('api.urls')),
    path('client/', include('client.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
