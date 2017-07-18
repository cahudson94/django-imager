"""."""
from django.contrib import admin
from imager_images.models import ImagerPhoto, ImagerAlbum

admin.site.register(ImagerPhoto)
admin.site.register(ImagerAlbum)
