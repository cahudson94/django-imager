"""imagersite URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from imager_profile.views import HomeView, LibraryView, ProfileView
from imager_images.views import PhotoCreate
from django.contrib.auth.decorators import login_required
from imager_images.views import (AlbumCreate, AlbumUpdate, AlbumDelete,
                                 PhotoCreate, PhotoUpdate, PhotoDelete)



urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/', ProfileView.as_view(), name='profile'),
    url(r'^images/library/', LibraryView.as_view(), name='library'),
    url(r'^images/upload/', PhotoCreate.as_view(), name='upload'),
    url(r'^update/(?P<pk>\d+)/$', login_required(PhotoUpdate.as_view()), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(PhotoDelete.as_view()), name='delete'),
    url(r'^album_create/$', login_required(AlbumCreate.as_view()), name='album_create'),
    url(r'^album_update/(?P<pk>\d+)/$', login_required(AlbumUpdate.as_view()), name='album_update'),
    url(r'^album_delete/(?P<pk>\d+)/$', login_required(AlbumDelete.as_view()), name='album_delete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
