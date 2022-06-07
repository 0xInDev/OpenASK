import email
import os

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.dispatch import receiver
from django.shortcuts import render
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection

from .models import *
from .forms import *
from .utils import *
from .serializers import *
from django.core import serializers as serializersCor

from django.db import transaction


class UserViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    has_user_field = False
    has_state = False
    filterset_fields = ["groups"]


class GroupViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    queryset = Group.objects.all()
    serializer_class = group_serializer
    permission_classes = [permissions.IsAdminUser]
    has_user_field = False
    has_state = False


class SondageViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
    queryset = Sondage.objects.filter(state=True)
    serializer_class = sondage_serializer
    filterset_fields = ['user']

    # get questions and labels for a sondage
    def getSondageData(self, id):
        response = []
        questions = Question.objects.filter(
            sondage=id).values("id", "type", "question")
        for label in questions:
            labels = QuestionLabel.objects.filter(
                question=label['id']).values("id", "label")
            label['reponses'] = list(labels)
            response.append(label)
        return response

    # get one sondage data title, question, possible answer
    @action(detail=True, methods=['GET'])
    def getSondage(self, request, pk):
        id = self.get_object().id
        sondage = self.get_object()
        # get sondage with question and possible answer
        allSondage = self.getSondageData(id)
        results = {'id': sondage.id, 'user': sondage.user.id,
                   'description': sondage.description, 'title': sondage.sondage, "questions": allSondage}
        results = json.dumps(results)
        return HttpResponse(results)

    #for verify a data type length ... on sondage creation
    def verifySondageDate(self, data):
        sondage = keyExistAndLength(data, 'title', 15 ) and keyExistAndLength(data, 'description', 30)
        if sondage is False : return "a question minlength is 15 characters" 
        for q in data['questions']:
            questionVerify = keyExistAndLength(q, 'question', 15)
            if questionVerify is False : return "a question minlength is 15 characters"
            if questionVerify:
                if q['type'] == 1:
                    if len(q['answers']) < 2:
                        return 'bad request answer list may be 2 or plus'
        return True     

    # transactional function for add sondage with json include sondage, question and question label
    # The format of json is in readme on github page of project
    @action(detail=False, methods=['Post'])
    @transaction.atomic
    def setSondage(self, request):
        data = request.data
        verification = self.verifySondageDate(data)
        if verification is not True: return Response(verification, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                user = User.objects.filter(id=data['user'])[0]
                obj1 = Sondage(sondage=data['title'], user=user,
                               description=data['description'])
                obj1.save()
                for q in data['questions']:
                    obj2 = Question(
                        sondage=Sondage.objects.last(), question=q['question'], type=q['type'], description=q['description'])
                    obj2.save()
                    tab = []
                    print(q)
                    for rep in q['answers']:
                        label = QuestionLabel(label=rep['label'],
                                              question=Question.objects.last())
                        tab.append(label)
                    QuestionLabel.objects.bulk_create(tab)

            return HttpResponse({"result": "Votre sondage a été enregistrer"})
        except:
            return HttpResponse({"result": "Votre sondage a été enregistrer"})

    # save answer of sondage
    @action(detail=False, methods=['Post'])
    @transaction.atomic
    def setAnswer(self, request):
        data = request.data
        tab = []
        sondage = Sondage.objects.filter(id=data['sondage'])[0]
        Answer.objects.filter(state=True).filter(question__type=1)
        for ans in data['answers']:
            question = Question.objects.filter(id=ans['id_question'])[0]
            if question.type  == 1:
                responses = QuestionLabel.objects.filter(id__in=ans['responses'])
                for res in responses:
                    answer = Answer(questionLabel=res, question = question,
                              response=res['response'], email=data['email']) 
                    tab.append(answer)
            if 'question_label' in ans :
                try:
                    questionL = QuestionLabel.objects.filter(
                    id=ans['question_label'])[0]
                except:
                    serializers.ValidationError('bad request question response don\'t exist ')
                    return Response('bad request question response don\'t exist ', status=status.HTTP_400_BAD_REQUEST)
            else:
                if len(ans['response']) > 3:
                    questionL = None
                else:
                    return Response('bad request incorrect label', status=status.HTTP_400_BAD_REQUEST)
            response = Answer(questionLabel=questionL, question = question,
                              response=ans['response'], email=data['email'])
            tab.append(response)
        Answer.objects.bulk_create(tab)

        return JsonResponse({"result": "Réponses enregistrer"})

    
    
    #on destroy implement logic delete by change state to false
    def destroy(self, request, *args, **kwargs):
        if self.has_state:
            instance = self.get_object()
            instance.state = False
            instance.save()
        else:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
    queryset = Question.objects.filter(state=True)
    serializer_class = question_serializer

    def destroy(self, request, *args, **kwargs):
        if self.has_state:
            instance = self.get_object()
            instance.state = False
            instance.save()
        else:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionLabelViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
    queryset = QuestionLabel.objects.filter(state=True)
    serializer_class = question_label_serializer

    def destroy(self, request, *args, **kwargs):
        if self.has_state:
            instance = self.get_object()
            instance.state = False
            instance.save() 
        else:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerViewSet(viewsets.ModelViewSet):
    has_user_field = True
    has_state = True
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
    queryset = Answer.objects.filter(state=True)
    serializer_class = answer_serializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['GET'])
    def countResponseSondage(self, request, pk):
        Answer.objects.filter()

    def destroy(self, request, *args, **kwargs):
        if self.has_state:
            instance = self.get_object()
            instance.state = False
            instance.save()
        else:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
