"""Profile models for imager app."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from imager_images.models import ImagerPhoto

CAMERA_CHOICES = [
    ('CN', 'Canon'),
    ('NK', 'Nikon'),
    ('KD', 'Kodak'),
    ('SN', 'Sony'),
    ('IP', 'iPhone')
]

PHOTO_CHOICES = [
    ('CR', 'Color'),
    ('BW', 'Black and White'),
    ('LS', 'Landscape'),
    ('PR', 'Portrait'),
    ('MI', 'Micro'),
    ('MA', 'Macro')
]


class ImageActiveProfile(models.Manager):
    """Get active profiles."""

    def get_queryset(self):
        """Get active profiles."""
        return super(ImageActiveProfile, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for user Django imager app."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(default='Seattle', max_length=25)
    state = models.CharField(default='WA', max_length=2)
    pic = models.ImageField(ImagerPhoto, upload_to='profile_pics')
    camera_type = models.CharField(
        max_length=2,
        choices=CAMERA_CHOICES,
    )
    photo_style = models.CharField(
        max_length=2,
        choices=PHOTO_CHOICES,
        default='CR'
    )
    job = models.CharField(default='', max_length=75)
    website = models.URLField(default='', max_length=255)
    objects = models.Manager()
    active = ImageActiveProfile()

    def active(self):
        """."""
        return self.user.is_active

    def __str__(self):
        """."""
        return """
        username: {}
        location: {}
        job: {}
        website: {}
        """.format(self.user.username, (self.city + ', ' + self.state), self.job, self.website)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
