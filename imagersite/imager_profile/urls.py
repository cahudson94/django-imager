"""URL managment for profile based pages."""
from django.conf.urls import url
from imager_profile.views import (
    ProfileView,
    PublicProfileView,
    ProfileEditView
)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', login_required(ProfileView.as_view()),
        name='profile'),
    url(r'^edit/$', ProfileEditView.as_view(),
        name='profile_edit'),
    url(r'^(?P<request_username>\w+\d*)/$',
        PublicProfileView.as_view(), name='public_profile'),
]
