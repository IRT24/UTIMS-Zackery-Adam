from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
                email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword123!')
            )
            self.stdout.write('Superuser has been created.')
        else:
            self.stdout.write('Superuser already exists.')
