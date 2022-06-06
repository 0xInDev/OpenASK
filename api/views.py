import email
import os

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
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection

from .models import *
from .forms import *
from .serializers import *
from django.core import serializers as serializersCor

from .base.viewset_helper import BaseViewset, HasAdminRole
from django.db import transaction


class UserViewSet(BaseViewset):

    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser | HasAdminRole]
    has_user_field = False
    has_state = False
    filterset_fields = ["groups"]


class GroupViewSet(BaseViewset):

    queryset = Group.objects.all()
    serializer_class = group_serializer
    permission_classes = [permissions.IsAdminUser | HasAdminRole]
    has_user_field = False
    has_state = False


class SondageViewSet(BaseViewset):
    queryset = Sondage.objects.filter(state=True)
    serializer_class = sondage_serializer
    filterset_fields = ['user']

    # get one sondage data title, question, possible answer
    @action(detail=True, methods=['GET'])
    def getSondage(self, request, pk):
        id = self.get_object().id
        sondage = self.get_object()
        u = self.getAllSondage(id)
        sondage = {'id': sondage.id, 'user': sondage.user.id,
                   'description': sondage.description, 'title': sondage.sondage, "questions": u}
        print(sondage)
        return HttpResponse(json.dumps(sondage))

    # transactional function for add sondage with json include sondage, question and question label
    # The format of json is in readme on github page of project
    @action(detail=False, methods=['Post'])
    @transaction.atomic
    def setSondage(self, request):
        data = request.data
        try:
            with transaction.atomic():
                user = User.objects.filter(id=data['user'])[0]
                obj1 = Sondage(sondage=data['title'], user=user,
                               description=data['description'])
                obj1.save(force_insert=True)
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

    @action(detail=False, methods=['Post'])
    @transaction.atomic
    def setAnswer(self, request):
        data = request.data
        tab = []
        sondage = Sondage.objects.filter(id=data['sondage'])[0]
        for ans in data['answers']:
            questionL = QuestionLabel.objects.filter(
                id=ans['question_label'])[0]
            print(type(questionL))
            response = Answer(questionLabel=questionL,
                              response=ans['label'], email=data['email'])
            tab.append(response)
        Answer.objects.bulk_create(tab)

        return HttpResponse({"result": "Réponses enregistrer"})

    def sqlListQuery(self, req):
        with connection.cursor() as cursor:
            cursor.execute(req)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    def getAllSondage(self, id):
        response = []
        query = "select ask.id, ask.type, ask.question from api_question ask where ask.sondage_id=" + \
            str(id)
        questions = self.sqlListQuery(query)

        for label in questions:
            queryQuestionLabel = "select label.id, label.label from api_questionlabel label where label.question_id=" + \
                str(label['id'])
            labels = self.sqlListQuery(queryQuestionLabel)
            label['reponses'] = labels
            response.append(label)

        return HttpResponse({"result": response})


class QuestionViewSet(BaseViewset):
    queryset = Question.objects.filter(state=True)
    serializer_class = question_serializer


class QuestionLabelViewSet(BaseViewset):
    queryset = QuestionLabel.objects.filter(state=True)
    serializer_class = question_label_serializer


class AnswerViewSet(BaseViewset):
    queryset = Answer.objects.filter(state=True)
    serializer_class = answer_serializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['GET'])
    def countResponseSondage(self, request, pk):
        Answer.objects.filter()


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
            if ext in ["mp4", "jpg", "jpeg", "png", "gif"]:
                handle_uploaded_file(request.FILES['file'], save_name)
            else:
                return HttpResponse(json.dumps({'status': 'Incorrect ext'}))
            return HttpResponse(json.dumps({'status': 'ok', 'file': save_name}))
    else:
        form = DocumentForm()  # A empty, unbound form

    return render(request, 'upload.html', {'form': form})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
