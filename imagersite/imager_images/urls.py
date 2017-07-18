"""."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from imager_images.views import (LibraryView,
                                 SinglePhotoView,
                                 SingleAlbumView,
                                 PhotoCreate,
                                 AlbumCreate,
                                 )


urlpatterns = [
    url(r'^library/', LibraryView.as_view(), name='library'),
    url(r'^photos/(?P<pk>\d+)/$', SinglePhotoView.as_view(),
        name='photo'),
    url(r'^albums/(?P<pk>\d+)/$', SingleAlbumView.as_view(),
        name='album'),
    url(r'^photo/add/', login_required(PhotoCreate.as_view()), name='add_photo'),
    url(r'^album/add/$', login_required(AlbumCreate.as_view()),
        name='add_album'),
]
