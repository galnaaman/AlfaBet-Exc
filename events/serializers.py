from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    creator = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())
    is_past = serializers.ReadOnlyField()
    popularity = serializers.ReadOnlyField(source='popularity_count')
    participants = serializers.SlugRelatedField(slug_field='id', many=True,read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creation_time', 'last_update', 'popularity', 'is_past', 'id']

    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        print(validated_data)
        validated_data.pop('popularity_count', None)
        return Event.objects.create(**validated_data)
