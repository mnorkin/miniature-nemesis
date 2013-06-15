from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
import uuid


class ProfileManager(models.Manager):
    """
    Profile Manager
    """
    def create_profile_by_email(self, email=None):
        """
        Creating user only with email
        """
        group, created = Group.objects.get_or_create(
            name='Subscriber'
        )
        user = User.objects.create_user(
            email,
            email,
            User.objects.make_random_password()
        )
        user.groups.add(group)
        user.is_staff = False
        user.save()


class Profile(models.Model):
    """
    User profiles
    """
    user = models.OneToOneField(User)
    uuid = models.CharField(
        max_length=200
    )
    objects = ProfileManager()


def create_user_profile(sender, instance, created, **kwargs):
    """
    Creating user profile
    """
    if created:
        profile, created = Profile.objects.get_or_create(
            user=instance,
            uuid=uuid.uuid4().hex
        )

post_save.connect(create_user_profile, sender=User)
