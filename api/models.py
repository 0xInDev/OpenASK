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
    libelle = models.CharField(max_length=255)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    verification = models.IntegerField(choices=((1, 'NO VERIFICATION'), (2, 'MI-STRICT'), (3, 'STRICT')), default=0)
   

    actif = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.RESTRICT, default=None)
    def __str__(self):
        return self.libelle

class Question(models.Model):
    libelle = models.CharField(max_length=255)
    type_response = models.IntegerField(choices=((0, 'CHOICE'), (1, 'CHOICES'), (3, 'NUMBER'), (2, 'TEXT')), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    sondage = models.ForeignKey('Sondage', on_delete=models.RESTRICT)

    def __str__(self):
        return self.libelle

class Person(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

class ResponseProposal(models.Model):
    libelle = models.CharField(max_length=255, null=True)
    value = models.BooleanField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    question = models.ForeignKey('Question', on_delete=models.RESTRICT, blank=False, null=False)

class Response(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    sondage = models.ForeignKey('Sondage', on_delete=models.RESTRICT)
    person = models.ForeignKey('Person', on_delete=models.RESTRICT, blank=False, null=False)

    def __str__(self):
        return "Response: {}".format(self.question.libelle)


class QuestionResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    choice_response = models.TextField()
    choices_response = models.TextField()
    number_response = models.IntegerField(null=True)
    text_response = models.IntegerField(null=True)
    
    question = models.ForeignKey('Question', on_delete=models.RESTRICT, blank=False, null=False)
    response = models.ForeignKey('Response', on_delete=models.RESTRICT, blank=False, null=False)

    def __str__(self):
        return "Response: {}".format(self.question.libelle)


