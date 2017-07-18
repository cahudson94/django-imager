"""View file for django imagerproject."""
from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from random import randint
import datetime


class HomeView(TemplateView):
    """."""

    template_name = "imagersite/home.html"

    def get_context_data(self, **kwargs):
        """."""
        photos = ImagerPhoto.objects.all()
        context = super(HomeView, self).get_context_data(**kwargs)
        if photos:
            random_index = randint(1, len(photos)) - 1
            random_photo = photos[random_index]
            title = random_photo.title
            description = random_photo.description
            date_uploaded = random_photo.date_uploaded
            user = random_photo.user.username
        else:
            random_photo = None
            title = 'Default'
            description = 'There are no uploaded pictures.'
            date_uploaded = datetime.datetime.now()
            user = ''
        context['user'] = context['view'].request.user
        context['random_photo'] = random_photo
        context['title'] = title
        context['description'] = description
        context['date'] = date_uploaded
        context['random_user'] = user
        return context


class ProfileView(ListView):
    """."""

    template_name = "imagersite/profile.html"
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        """."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        current_user = context['view'].request.user
        user = ImagerProfile.objects.get(user=current_user)
        pub_pics = (ImagerPhoto.objects
                    .filter(user=current_user)
                    .filter(published='PB')).count()
        pub_albums = (ImagerAlbum.objects
                      .filter(user=current_user)
                      .filter(published='PB')).count()
        prv_pics = (ImagerPhoto.objects
                    .filter(user=current_user)
                    .filter(published='PV')).count()
        prv_albums = (ImagerAlbum.objects
                      .filter(user=current_user)
                      .filter(published='PV')).count()
        context['username'] = user.user
        context['location'] = (user.city + ', ' + user.state)
        context['pic'] = user.pic
        context['job'] = user.job
        context['camera'] = user.camera_type
        context['photostyle'] = user.photography_style
        context['website'] = user.website
        context['pub_pics'] = pub_pics
        context['pub_albums'] = pub_albums
        context['prv_pics'] = prv_pics
        context['prv_albums'] = prv_albums
        return context


class PublicProfileView(ListView):
    """."""

    template_name = "imagersite/other_profile.html"
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        """."""
        context = super(PublicProfileView, self).get_context_data(**kwargs)
        current_user = context['view'].request.user
        request_user = User.objects.filter(username=self.kwargs['request_username'])
        profile = ImagerProfile.objects.get(user=request_user)
        pub_pics = (ImagerPhoto.objects
                    .filter(user=current_user)
                    .filter(published='PB')).count()
        pub_albums = (ImagerAlbum.objects
                      .filter(user=current_user)
                      .filter(published='PB')).count()
        context['user'] = current_user
        context['username'] = profile.user
        context['request_user'] = request_user
        context['location'] = (profile.city + ', ' + profile.state)
        context['pic'] = profile.pic
        context['job'] = profile.job
        context['camera'] = profile.camera_type
        context['photostyle'] = profile.photography_style
        context['website'] = profile.website
        context['pub_pics'] = pub_pics
        context['pub_albums'] = pub_albums
        return context
