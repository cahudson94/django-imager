"""."""
from django.conf.urls import url
from imager_images.views import photo_view, album_view, library_view

urlpatterns = [
    url(r'^library/', library_view, name='library'),
    url(r'^photos/(?P<photo_id>\d+)/$', photo_view, name='photo'),
    url(r'^albums/(?P<album_id>\d+)/$', album_view, name='album')
]
