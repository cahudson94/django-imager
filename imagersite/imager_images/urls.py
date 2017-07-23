"""URL file for image based pages."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from imager_images.views import (LibraryView,
                                 SinglePhotoView,
                                 SingleAlbumView,
                                 PhotoCreate,
                                 AlbumCreate,
                                 PhotoEdit,
                                 AlbumEdit,
                                 PhotoTagListView,
                                 AlbumTagListView,
                                 PhotosView,
                                 AlbumsView
                                 )


urlpatterns = [
    url(r'^library/', login_required(LibraryView.as_view()),
        name='library'),
    url(r'^photos/$', PhotosView.as_view(), name='photos'),
    url(r'^albums/$', AlbumsView.as_view(), name='albums'),
    url(r'^photos/(?P<pk>\d+)/$', login_required(SinglePhotoView.as_view()),
        name='photo'),
    url(r'^albums/(?P<pk>\d+)/$', login_required(SingleAlbumView.as_view()),
        name='album'),
    url(r'^photos/tags/(?P<slug>\w*\d*)/$', login_required(PhotoTagListView.as_view()),
        name='tagged_photos'),
    url(r'^albums/tags/(?P<slug>\w*\d*)/$', login_required(AlbumTagListView.as_view()),
        name='tagged_albums'),
    url(r'^photo/add/$', login_required(PhotoCreate.as_view()),
        name='add_photo'),
    url(r'^album/add/$', login_required(AlbumCreate.as_view()),
        name='add_album'),
    url(r'^photo/(?P<pk>\d+)/edit/$', login_required(PhotoEdit.as_view()),
        name='edit_photo'),
    url(r'^album/(?P<pk>\d+)/edit/$', login_required(AlbumEdit.as_view()),
        name='edit_album'),
]
