from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from rest_framework import routers

from api import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Open SOndage API')

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='Open SOndage API'))
]
