from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creation_time', 'last_update', 'popularity', 'is_past']
        depth = 1