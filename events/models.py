from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    """
    Event model - represents a single event
    """
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    # Location and venue can be usesd as geo fields need to change it later
    location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)

    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)

    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def popularity(self):
        return self.participants.count()

    @property
    def is_past(self):
        return self.end_time < timezone.now()

    class Meta:
        db_table = "events"
        ordering = ['id']

