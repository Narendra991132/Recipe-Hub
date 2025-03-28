from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Creates missing user profiles'

    def handle(self, *args, **options):
        users_without_profiles = []
        
        for user in User.objects.all():
            try:
                # Try to access the profile
                user.profile
            except User.profile.RelatedObjectDoesNotExist:
                # If profile doesn't exist, add user to the list
                users_without_profiles.append(user)
        
        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS('All users already have profiles.'))
            return
            
        # Create profiles for users without profiles
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
            
        self.stdout.write(self.style.SUCCESS(f'Created {len(users_without_profiles)} missing profiles.'))