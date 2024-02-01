from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    creator = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creation_time', 'last_update', 'popularity', 'is_past', 'id']
        depth = 1
