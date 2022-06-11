import email
import os
import json

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.dispatch import receiver
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from rest_framework.response import Response as RestReponse

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .utils import *
from .serializers import *

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
	queryset = Sondage.objects.all()
	filter_backends = [DjangoFilterBackend]
	serializer_class = SondageSerializer
	pagination_class = None
	permission_classes = [permissions.AllowAny]

	@action(detail=True)
	def result(self, request, pk=None):
		sondage = self.get_object()
		data = {}
		data['sondage'] = SondageSerializer(sondage, context={"request":request}).data
		_questions = []
		for question in Question.objects.filter(sondage=sondage):
			_questions.append({
				"id": question.id, 
				"libelle": question.libelle, 
				"type_response": question.type_response
				})
		_responses = []

		for response in Response.objects.filter(sondage=sondage):
			_response_data = {}
			_response_data['author'] = PersonSerializer(response.person, context={"request":request}).data
			_author_response = []
			for question_response in QuestionResponse.objects.filter(response=response):
				question = question_response.question
				_question_response_data = {"question_libelle":question.libelle, "question_id": question.id}
				if question.type_response == 0:
					_question_response_data['response'] = json.loads(question_response.choice_response)
				elif question.type_response == 1:
					_question_response_data['response'] = json.loads(question_response.choices_response)
				elif question.type_response == 2:
					_question_response_data['response'] = question_response.text_response
				elif question.type_response == 3:
					_question_response_data['response'] = int(question_response.number_response)
				else:
					_question_response_data['response'] = {"status": "Failed to understand this answer"}
				_author_response.append(_question_response_data)
				
			_response_data['author_response'] = _author_response
			_responses.append(_response_data)



		data['sondage']['questions'] = _questions
		data['sondage']['responses'] = _responses

		return RestReponse(data)

class QuestionViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.AllowAny]
	queryset = Question.objects.all()
	serializer_class = QuestionGetSerializer
	filterset_fields = ["sondage"]

	def list(self, request):
		if "sondage" in request.GET and request.GET['sondage'] != "":
			return super().list(self, request)
		else:
			serializer = self.get_serializer_class()(Question.objects.none(), many=True)
			return RestReponse(serializer.data)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return QuestionPostSerializer
		else:
			return QuestionGetSerializer

class ResponseProposalViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.AllowAny]
	queryset = ResponseProposal.objects.all()
	pagination_class = None
	serializer_class = ResponseProposalGetSerializer
	filterset_fields = ["question"]

	def list(self, request):
		if "question" in request.GET and request.GET['question'] != "":
			return super().list(self, request)
		else:
			return RestReponse(self.get_serializer_class()(ResponseProposal.objects.none(), many=True).data)
	
	def get_serializer_class(self):
		if self.request.method == 'POST':
			return ResponseProposalPostSerializer
		else:
			return ResponseProposalGetSerializer

class PersonViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.AllowAny]
	queryset = Person.objects.all()
	pagination_class = None
	serializer_class = PersonSerializer

	def list(self, request):
		serializer = PersonSerializer(Person.objects.none(), many=True)
		return RestReponse(serializer.data)

class ResponseViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.AllowAny]
	queryset = Response.objects.all()
	pagination_class = None
	serializer_class = ResponseGetSerializer
	filterset_fields = ["sondage"]

	def list(self, request):
		if "sondage" in request.GET and request.GET['sondage'] != "":
			return super().list(self, request)
		else:
			serializer = self.get_serializer_class()(Response.objects.none(), many=True)
			return RestReponse(serializer.data)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return ResponsePostSerializer
		else:
			return ResponseGetSerializer

class QuestionResponseViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.AllowAny]
	queryset = QuestionResponse.objects.all()
	pagination_class = None
	serializer_class = QuestionResponseGetSerializer
	filterset_fields = ["question"]

	def list(self, request):
		if "question" in request.GET and request.GET['question'] != "":
			return super().list(self, request)
		else:
			serializer = self.get_serializer_class()(Question.objects.none(), many=True)
			return RestReponse(serializer.data)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return QuestionResponsePostSerializer
		else:
			return QuestionResponseGetSerializer

  
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
