from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from ..models import Event


class EventViewTest(TestCase):
    """
    Test case for the Event view.
    """

    def setUp(self):
        """
        Set up the test case with a user and an event.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        participant = User.objects.create_user(username='participant', password='testpassword')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            creator=self.user,
            name='Test Event',
            description='This is a test event',
            location='Test Location',
            venue='Test Venue',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )
        self.event.save()
        self.event.participants.add(participant)

    def test_event_creation_successful(self):
        """
        Test the successful creation of an event.
        """
        response = self.client.post('/api/v1/events/', {
            "creator": self.user.id,
            "name": "Community Meetup",
            "description": "A community meetup to discuss various topics of interest.",
            "location": "Central Park",
            "venue": "The Great Lawn",
            "start_time": "2024-06-15T15:00:00Z",
            "end_time": "2024-06-15T17:00:00Z",
            "participants": []

        },"json")
        self.assertEqual(response.status_code, 201)

    def test_event_creation_missing_field(self):
        """
        Test the creation of an event with a missing field.
        """
        response = self.client.post('/api/v1/events/', {
            'name': 'New Event',
            'description': 'This is a new event',
            'location': 'New Location',
            'venue': 'New Venue',
            'start_time': timezone.now(),
        })
        self.assertEqual(response.status_code, 400)

    def test_event_detail_retrieval_successful(self):
        """
        Test the successful retrieval of an event detail.
        """
        response = self.client.get(f'/api/v1/events/{self.event.id}')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_retrieval_nonexistent(self):
        """
        Test the retrieval of a nonexistent event detail.
        """
        response = self.client.get('/api/v1/events/99999')
        self.assertEqual(response.status_code, 404)

    def test_event_deletion_successful(self):
        """
        Test the successful deletion of an event.
        """
        response = self.client.delete(f'/api/v1/events/{self.event.id}')
        self.assertEqual(response.status_code, 204)

    def test_event_deletion_nonexistent(self):
        """
        Test the deletion of a nonexistent event.
        """
        response = self.client.delete('/api/v1/events/9999')
        self.assertEqual(response.status_code, 404)

    def test_event_subscription_successful(self):
        """
        Test the successful subscription to an event.
        """
        response = self.client.post(f'/api/v1/events/{self.event.id}/subscribe/', {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_event_subscription_already_subscribed(self):
        """
        Test the subscription to an event when already subscribed.
        """
        self.event.participants.add(self.user)
        response = self.client.post(f'/api/v1/events/{self.event.id}/subscribe/', {'user_id': self.user.id})
        self.assertEqual(response.status_code, 400)

    def test_batch_events_create_successful(self):
        """
        Test the successful creation of events in batch.
        """
        response = self.client.post('/api/v1/events/batch/', [
            {
                "creator": self.user.id,
                "name": "Community Meetup",
                "description": "A community meetup to discuss various topics of interest.",
                "location": "Central Park",
                "venue": "The Great Lawn",
                "start_time": "2024-06-15T15:00:00Z",
                "end_time": "2024-06-15T17:00:00Z",
                "participants": []
            },
            {
                "creator": self.user.id,
                "name": "Community Meetup 2",
                "description": "A community meetup to discuss various topics of interest.",
                "location": "Central Park",
                "venue": "The Great Lawn",
                "start_time": "2024-06-15T15:00:00Z",
                "end_time": "2024-06-15T17:00:00Z",
                "participants": []
            }
        ], format='json')
        self.assertEqual(response.status_code, 201)