import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if one does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')

        if not email or not password:
            self.stdout.write('DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD not set, skipping.')
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f'Superuser {email} already exists, skipping.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='ADMIN',
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully.'))
