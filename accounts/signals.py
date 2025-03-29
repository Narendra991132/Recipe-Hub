from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update a User profile
    """
    # Try to get profile and create if it doesn't exist
    try:
        # If profile exists, just save it
        instance.profile.save()
    except Profile.DoesNotExist:
        # If profile doesn't exist, create it
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the user is saved
    """
    # Check if profile exists before saving to avoid errors
    if hasattr(instance, 'profile'):
        instance.profile.save()