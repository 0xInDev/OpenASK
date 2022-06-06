from rest_framework import permissions, serializers, viewsets
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.utils import serializer_helpers


class HasAdminRole(permissions.BasePermission):

    def has_permission(self, request, view):

        user = request.user
        return user.groups.filter(name='ADMIN').exists()


class BaseViewset(viewsets.ModelViewSet):

    has_user_field = True
    has_state = True
    serializer_classes = []

    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if len(self.serializer_classes) == 0:
            return self.serializer_class
        else:
            if self.request.method == 'GET':
                return self.serializer_classes[0]
            return self.serializer_classes[1]

    def perform_create(self, serializer):
        if self.has_user_field:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        if self.has_state:
            instance = self.get_object()
            instance.state = False
            instance.save()
        else:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
