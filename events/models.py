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
    location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)

    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)

    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    popularity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.end_time < self.start_time:
            raise ValueError("End time cannot be before start time")
        if self.id is None:
            self.popularity = 0
        else:
            self.popularity = self.popularity_count
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def popularity_count(self):
        return self.participants.count()

    @property
    def is_past(self):
        return self.end_time < timezone.now()

    class Meta:
        db_table = "events"
        ordering = ['id']
