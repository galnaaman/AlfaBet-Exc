from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create specified number of fake users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='The number of fake users to create')

    def handle(self, *args, **kwargs):
        num_users = kwargs['num_users']
        faker = Faker()

        for _ in range(num_users):
            username = faker.user_name()
            email = faker.email()
            password = faker.password()
            User.objects.create_user(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_users} fake users'))
