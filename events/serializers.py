from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    """
    Event Serializer
    """
    creator = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())
    # participants = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all(), many=True)
    is_past = serializers.ReadOnlyField()
    popularity = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creation_time', 'last_update', 'popularity', 'is_past', 'id']

    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        print(validated_data)
        return Event.objects.create(**validated_data)
