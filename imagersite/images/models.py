"""Models for images for our users."""
from django.db import models


class Image(models.Model):
    """Image properties."""

    date = models.DateField()
