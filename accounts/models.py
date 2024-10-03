from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('writer', 'Writer'),
        ('commenter', 'Commenter'),
        ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)  # Optional bio field

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class UserPasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
