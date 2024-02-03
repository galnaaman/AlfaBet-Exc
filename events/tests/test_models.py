from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Event


class EventModelTest(TestCase):
    """
    Test case for the Event model.
    """

    def setUp(self):
        """
        Set up the test case with a user and an event.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.event = Event.objects.create(
            creator=self.user,
            name='Test Event',
            description='This is a test event',
            location='Test Location',
            venue='Test Venue',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_event_creation(self):
        """
        Test the creation of an event.
        """
        self.assertEqual(self.event.creator, self.user)
        self.assertEqual(self.event.name, 'Test Event')
        self.assertEqual(self.event.description, 'This is a test event')
        self.assertEqual(self.event.location, 'Test Location')
        self.assertEqual(self.event.venue, 'Test Venue')
        self.assertEqual(self.event.start_time.date(), timezone.now().date())
        self.assertEqual(self.event.end_time.date(), (timezone.now() + timezone.timedelta(hours=1)).date())
        self.assertEqual(self.event.popularity, 0)

    def test_popularity_count(self):
        """
        Test the popularity count of an event.
        """
        self.assertEqual(self.event.popularity_count, 0)
        self.event.participants.add(self.user)
        self.assertEqual(self.event.popularity_count, 1)

    def test_is_past(self):
        """
        Test if an event is past.
        """
        self.assertFalse(self.event.is_past)
        self.event.end_time = timezone.now() - timezone.timedelta(hours=1)
        self.assertTrue(self.event.is_past)

    def test_popularity_negitive(self):
        """
        Test the popularity count when a participant is removed.
        """
        self.assertEqual(self.event.popularity_count, 1)
        self.event.participants.remove(self.user)
        self.event.save()
        self.assertEqual(self.event.popularity_count, 0)
