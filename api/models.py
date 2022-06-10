from django.db import models
from django.conf import settings

def logged_user(request):
    current_user = request.user
    return current_user


class Sondage(models.Model):
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sondage = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    theme = models.JSONField(default=dict)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.RESTRICT, default=None)

    def __str__(self):
        return self.sondage


class Question(models.Model):
    state = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sondage = models.ForeignKey('Sondage', on_delete=models.RESTRICT)
    question = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    type = models.IntegerField(
        choices=((0, 'CHOICE'), (1, 'CHOICES'), (3, 'NUMBER'), (2, 'TEXT')), default=0)

    def __str__(self):
        return self.question


class QuestionLabel(models.Model):
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey('Question', on_delete=models.RESTRICT)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Answer(models.Model):
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questionLabel = models.ForeignKey(
        'QuestionLabel', on_delete=models.RESTRICT, blank=True, null=True)
    question = models.ForeignKey(
        'Question', on_delete=models.RESTRICT, blank=True, null=True)
    response = models.CharField(max_length=255, null=True, default="")
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.questionLabel


