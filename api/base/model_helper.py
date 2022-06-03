from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def logged_user(request):
    current_user = request.user
    return current_user


class BaseModel(models.Model):

    state = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def foreign(class_name, on_delete=models.RESTRICT, **kwargs):
    return models.ForeignKey(class_name, on_delete=on_delete, **kwargs)
