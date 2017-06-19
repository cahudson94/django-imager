"""."""
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from location_field.models.plain import PlainLocationField


class ImagerProfile(models.Model):
    """A profile for user to use our application."""

    user = models.OneToOneField(User)
    # user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    camera_type = models.CharField(max_length=75)
    photography_style = models.CharField(default='', max_length=255)
    job = models.CharField(default='', max_length=75)
    website = models.CharField(default='', max_length=255)
    user.is_active = bool(True)

    def active(self):
        """."""
        query = User.objects.all()
        active_users = []
        for user in query:
            if user.is_active:
                active_users.append(user)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
