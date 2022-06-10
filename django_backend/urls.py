from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
