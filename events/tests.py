from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')
        self.user.save()
        self.event = Event.objects.create(
            creator=self.user,
            name='Test Event',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

        self.event.save()

    def test_event_creation_is_successful(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.name, 'Test Event')

    def test_event_popularity_count_increases_when_user_participates(self):
        self.event.participants.add(self.user)
        self.assertEqual(self.event.popularity_count, 1)

    def test_event_is_past_when_end_time_is_in_the_past(self):
        self.event.start_time= timezone.now() - timezone.timedelta(hours=2)
        self.event.end_time = timezone.now() - timezone.timedelta(hours=1)
        self.event.save()
        self.assertTrue(self.event.is_past)

    def test_event_start_time_cannot_be_after_end_time_raises_error(self):
        with self.assertRaises(ValueError):
            self.event.start_time = timezone.now() + timezone.timedelta(hours=1)
            self.event.end_time = timezone.now()
            self.event.save()

    def test_event_popularity_defaults_to_zero_on_creation(self):
        self.assertEqual(self.event.popularity, 0)
