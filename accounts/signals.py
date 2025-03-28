from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile whenever a new User is created
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the user is saved
    """
    # Check if profile exists to avoid error
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        # Create profile if it doesn't exist
        Profile.objects.create(user=instance)