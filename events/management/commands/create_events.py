from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Event  # Replace with your actual Event model path
from faker import Faker
from random import choice
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create specified number of fake events'

    def add_arguments(self, parser):
        parser.add_argument('num_events', type=int, help='The number of fake events to create')

    def handle(self, *args, **kwargs):
        num_events = kwargs['num_events']
        faker = Faker()

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
            return

        for _ in range(num_events):
            creator = choice(users)
            name = faker.text(max_nb_chars=20)
            description = faker.text()
            start_time = timezone.now()
            end_time = start_time + timedelta(minutes=35)
            Event.objects.create(creator=creator, name=name, description=description, start_time=start_time, end_time=end_time)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_events} fake events'))
