from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'password', 'groups', 'url']

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data.get('password'))
        return super().update(instance, validated_data)



class permission_serializer(serializers.ModelSerializer):

    class Meta:
        model = Permission


class group_serializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ['permissions']


class SondageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Sondage
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['url_slug'] = slugify(validated_data['libelle'])
        return super(SondageSerializer, self).create(validated_data)


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

class QuestionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

class QuestionGetSerializer(serializers.ModelSerializer):
    sondage = SondageSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class ResponseProposalGetSerializer(serializers.ModelSerializer):
    value = serializers.HiddenField(default=False)
    question = QuestionPostSerializer()
    class Meta:
        model = ResponseProposal
        fields = '__all__'

class ResponseProposalPostSerializer(serializers.ModelSerializer):
    value = serializers.HiddenField(default=False)
    class Meta:
        model = ResponseProposal
        fields = '__all__'


class ResponseGetSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    sondage = SondageSerializer(read_only=True)
    class Meta:
        model = Response
        fields = '__all__'

class ResponsePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


class QuestionResponseGetSerializer(serializers.ModelSerializer):
    question = QuestionGetSerializer(read_only=True)
    sondage = SondageSerializer(read_only=True)
    class Meta:
        model = QuestionResponse
        fields = '__all__'

class QuestionResponsePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = '__all__'



# class answer_serializer(serializers.ModelSerializer):
#     state = serializers.HiddenField(default=True)

#     class Meta:
#         model = Answer
#         fields = '__all__'


