from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPasswordHistory

@receiver(post_save, sender=User)
def save_user_password_history(sender, instance, **kwargs):
    # Check if it's a new user or if the password has changed
    if kwargs.get('created', False) or instance.password != instance.__class__.objects.get(pk=instance.pk).password:
        UserPasswordHistory.objects.create(
            user=instance,
            password=instance.password
        )
