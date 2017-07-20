"""View file for django imagerproject."""
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.models import User
from random import randint
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from imager_profile.forms import ProfileForm
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

    template_name = "imager_profile/profile.html"
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
        context['camera'] = user.get_camera_type_display()
        context['photostyle'] = user.get_photo_style_display()
        context['website'] = user.website
        context['pub_pics'] = pub_pics
        context['pub_albums'] = pub_albums
        context['prv_pics'] = prv_pics
        context['prv_albums'] = prv_albums
        return context


class PublicProfileView(ListView):
    """."""

    template_name = "imager_profile/other_profile.html"
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
        context['photostyle'] = profile.photo_style
        context['website'] = profile.website
        context['pub_pics'] = pub_pics
        context['pub_albums'] = pub_albums
        return context


class ProfileEditView(UpdateView):
    """View for editing the users profile."""

    model = User
    template_name = 'imager_profile/edit_profile.html'
    success_url = reverse_lazy('profile')
    fields = []

    def get_object(self):
        """Return the user."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Set the form."""
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context['form'] = ProfileForm()

    def post(self, request, *args, **kwargs):
        """Set the new info."""
        self.object = self.get_object()
        user = request.user
        info = request.POST
        if info['username'] and info['email']:
            if info['username']:
                user.username = info['username']
            else:
                user.username = user.username
            if info['email']:
                user.email = info['email']
            else:
                user.email = user.email
            if 'first_name' in info.keys():
                user.first_name = info['first_name']
            else:
                user.first_name = user.first_name
            if 'last_name' in info.keys():
                user.last_name = info['last_name']
            else:
                user.last_name = user.last_name
            if 'photo_style' in info.keys():
                user.imagerprofile.photo_style = info['photo_style']
            else:
                user.imagerprofile.photo_style = user.imagerprofile.photo_style
            if 'camera_type' in info.keys():
                user.imagerprofile.camera_type = info['camera_type']
            else:
                user.imagerprofile.camera_type = user.imagerprofile.camera_type
            if 'job' in info.keys():
                user.imagerprofile.job = info['job']
            else:
                user.imagerprofile.job = user.imagerprofile.job
            if 'website' in info.keys():
                user.imagerprofile.website = info['website']
            else:
                user.imagerprofile.website = user.imagerprofile.website
            user.save()
            user.imagerprofile.save()

            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(**kwargs))
