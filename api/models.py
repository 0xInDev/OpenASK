from django.db import models
from django.conf import settings
 
def logged_user(request):
    current_user = request.user 
    return current_user


class Sondage(models.Model):
    """
    verificaiton:    
        Verification level 1 : give to any visitor to add new sondage answer without any verification
        Verification level 2 : check the unicity of email address in sondage answer
        Verificaiton level 3 : Email verification with validation code is asked.

    """
    url_slug = models.CharField(max_length=255, unique=True, default="(NIL)")
    libelle = models.CharField(max_length=255)
    description = models.TextField(null=True)
    verification = models.IntegerField(choices=((1, 'NO VERIFICATION'), (2, 'MI-STRICT'), (3, 'STRICT')), default=0)

    actif = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.libelle

class Question(models.Model):
    libelle = models.CharField(max_length=255)
    type_response = models.IntegerField(choices=((0, 'CHOICE'), (1, 'CHOICES'), (2, 'TEXT'), (3, 'NUMBER')), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sondage = models.ForeignKey('Sondage', on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class Person(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.email == None:
            return "Person {}".format(self.id)
        return "Person {}".format(self.email)

class ResponseProposal(models.Model):
    libelle = models.CharField(max_length=255, null=False, default="")
    value = models.BooleanField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=False, null=False)

class Response(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sondage = models.ForeignKey('Sondage', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return "Response: {}".format(self.id)

class QuestionResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    choice_response = models.IntegerField(null=True, blank=True)
    choices_response = models.TextField(null=True, blank=True)
    number_response = models.IntegerField(null=True, blank=True)
    text_response = models.TextField(null=True, blank=True)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=False, null=False)
    response = models.ForeignKey('Response', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return "Response: {}".format(self.id)


