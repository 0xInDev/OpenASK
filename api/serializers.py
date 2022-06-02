from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from numpy import product
from .models import *
from rest_framework import serializers

from .base import serialize_helper as sz


permission_serializer = sz.generate_serializer(Permission)


group_serializer = sz.generate_serializer(
    Group, ['permissions'], g_serializer=serializers.ModelSerializer)

sondage_serializer = sz.generate_serializer(Sondage)

question_serializer = sz.generate_serializer(Question)

question_label_serializer = sz.generate_serializer(QuestionLabel)

answer_serializer = sz.generate_serializer(Answer)


class UserSerializer(sz.DefaultSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
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
            #print(validated_data )
            validated_data['password'] = make_password(
                validated_data.get('password'))
        return super().update(instance, validated_data)
