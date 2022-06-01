from collections import defaultdict
from rest_framework import serializers

class DefaultSerializer(serializers.ModelSerializer):
    state = serializers.HiddenField(default=True)
    
def generate_serializer(g_model, g_exclude = [], g_depth = 0, g_create = lambda g_y, g_x: g_x, g_serializer=DefaultSerializer):

    class Serializer(g_serializer):

        class Meta:
            model  = g_model
            exclude  = g_exclude
            depth = g_depth

        def create(self, validated_data):
            return super().create(g_create(self, validated_data))

    return Serializer
