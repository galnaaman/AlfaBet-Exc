from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    creator = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=False)
    is_past = serializers.ReadOnlyField()
    popularity = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creation_time', 'last_update', 'popularity', 'is_past', 'id']

