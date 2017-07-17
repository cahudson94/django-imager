"""."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from sorl.thumbnail import ImageField


PUBLISHED_STATUS = (
    ('PB', 'public'),
    ('PV', 'private'),
    ('SH', 'shared'),
)


@python_2_unicode_compatible
class ImagerPhoto(models.Model):
    """Photo models for Django imager app."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='photos')
    photo = ImageField(upload_to='images')
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    title = models.CharField(default='', max_length=50)


@python_2_unicode_compatible
class ImagerAlbum(models.Model):
    """Album models for Django imager app."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='albums')
    title = models.CharField(default='', max_length=50)
    photos = models.ManyToManyField(ImagerPhoto, blank=True,
                                    default='', related_name='albums')
    cover = models.ForeignKey(ImagerPhoto, blank=True, null=True,
                              related_name='+')
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
