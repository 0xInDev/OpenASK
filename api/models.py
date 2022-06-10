from django.db import models
from django.conf import settings

def logged_user(request):
    current_user = request.user
    return current_user


class Sondage(models.Model):
    sondage = models.CharField(max_length=255)
    description = models.Text(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.RESTRICT, default=None)
    
    strictValidation = models.BooleanField(default=False)
    state = models.IntegerField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.sondage


class Question(models.Model):
    
    sondage = models.ForeignKey('Sondage', on_delete=models.RESTRICT)
    question = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    type = models.IntegerField(
        choices=((0, 'CHOICE'), (1, 'CHOICES'), (3, 'NUMBER'), (2, 'TEXT')), default=0)

    state = models.IntegerField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    state = models.BooleanField(default=True)
    
    question = models.ForeignKey(
        'Question', on_delete=models.RESTRICT, blank=True, null=True)
    response = models.CharField(max_length=255, null=True, default="")
    email = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


