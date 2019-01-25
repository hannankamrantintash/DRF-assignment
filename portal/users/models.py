from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from users.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    """
        Custom User Model
    """
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cnic = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Post(models.Model):
    """
        User Posting Data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, **kwargs):
    """Creates token for the new user"""
    if created:
        Token.objects.create(user=instance)
