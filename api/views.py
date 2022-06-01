import os
<<<<<<< HEAD

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.template import RequestContext
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import render
from django.conf import settings


from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .forms import *
from .serializers import *

from .serializers import *
from .models import *
from .forms import *

from .base.viewset_helper import BaseViewset, HasAdminRole, HasAgentRole

class UserViewSet(BaseViewset):

    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser | HasAdminRole]
    has_user_field = False
    has_state = False
    filterset_fields = ["groups"]

    @action(detail=False, methods=['GET'])
    def free_technician(self, request):
        user = User.objects.filter(groups__id__exact=2, is_active = True)
        return Response({'results': UserSerializer2(user, many=True).data})

class GroupViewSet(BaseViewset):

    queryset = Group.objects.all()
    serializer_class = group_serializer
    permission_classes = [permissions.IsAdminUser | HasAdminRole]
    has_user_field = False
    has_state = False


def handle_uploaded_file(f, name):
    path = os.path.join(settings.MEDIA_ROOT, name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            ext = request.FILES['file'].name.split(".")[-1]
            if len(request.FILES['file'].name.split(".")) < 2:
                ext = "png"
            save_name = str(uuid.uuid4()) + "." + ext
            if ext in ["mp4","jpg","jpeg","png","gif"]:
                handle_uploaded_file(request.FILES['file'], save_name)
            else: 
                return HttpResponse(json.dumps({'status': 'Incorrect ext'}))
            return HttpResponse(json.dumps({'status':'ok', 'file': save_name }))
    else:
        form = DocumentForm()  # A empty, unbound form

    return render(request, 'upload.html', {'form': form})
 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
