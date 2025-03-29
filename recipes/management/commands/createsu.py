from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword123'
            )
            # Create profile manually
            Profile.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS('Superuser has been created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))