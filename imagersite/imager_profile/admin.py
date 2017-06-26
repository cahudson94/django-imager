"""Allows access to django admin page."""
from django.contrib import admin
from imager_profile.models import ImagerProfile

admin.site.register(ImagerProfile)
