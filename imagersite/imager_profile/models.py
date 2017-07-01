"""Profile models for imager app."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from imager_images.models import ImagerPhoto, ImagerAlbum

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
    city = models.CharField(default='', max_length=25)
    state = models.CharField(default='', max_length=2)
    pic = models.ImageField(ImagerPhoto, upload_to='profile_pics')
    camera_type = models.CharField(
        max_length=2,
        choices=CAMERA_CHOICES,
    )
    photography_style = models.CharField(
        max_length=5,
        choices=PHOTO_CHOICES,
        default='CR'
    )
    job = models.CharField(default='', max_length=75)
    website = models.CharField(default='', max_length=255)
    pub_pics = ImagerPhoto.objects.filter(published='PB').all().count()
    pub_albums = ImagerAlbum.objects.filter(published='PB').all().count()
    prv_pics = ImagerPhoto.objects.filter(published='PV').all().count()
    prv_albums = ImagerAlbum.objects.filter(published='PV').all().count()
    objects = models.Manager()
    active = ImageActiveProfile()

    def active(self):
        """."""
        return self.user.is_active

    # def __repr__(self):
    #     """."""
    #     return """
    # username: {}
    # location: {}
    # camera_type: {}
    # photography_style: {}
    # job: {}
    # website: {}
    #     """.format(
    #         self.user.username,
    #         self.location,
    #         self. camera_type,
    #         self.photography_style,
    #         self.job,
    #         self.website
    #     )


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
