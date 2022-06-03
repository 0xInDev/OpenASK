from email.policy import default
from statistics import mode
from unicodedata import name
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
import json
from datetime import date

from .base import model_helper as base


def logged_user(request):
    current_user = request.user
    return current_user


class Document(base.BaseModel):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class Sondage(base.BaseModel):
    sondage = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    theme = models.JSONField(default=dict)
    user = base.foreign(settings.AUTH_USER_MODEL,
                        on_delete=models.RESTRICT, default=None)

    def __str__(self):
        return self.sondage


class Question(base.BaseModel):
    sondage = base.foreign('Sondage')
    question = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    #user = base.foreign(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT, default=None)
    type = models.IntegerField(
        choices=((0, 'checkbox'), (1, 'multiple choice'), (2, 'text')), default=0)

    def __str__(self):
        return self.question


class QuestionLabel(base.BaseModel):
    question = base.foreign('Question')
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Answer(base.BaseModel):
    questionLabel = base.foreign('QuestionLabel')
    response = models.CharField(max_length=255, null=True, default="")
    email = models.CharField(max_length=255)
    #type = models.CharField(max_length=255)

    def __str__(self):
        return self.questionLabel


# PRODUCT SESSION
