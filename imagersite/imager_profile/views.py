"""View file for django imagerproject."""
from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto
from django.views.generic import TemplateView, ListView
# from django.views import View
# from django.template import loader


class HomeView(TemplateView):
    template_name = "imagersite/home.html"

    def get_context_data(self):
        return {}


def account_view(request):
    """Registration view for imager."""
    return render(request, 'imagersite/accounts.html')


class AccountView(TemplateView):
    template_name = "imagersite/accounts.html"

    def get_context_data(self):
        return {}


class ProfileView(ListView):
    template_name = "imagersite/profile.html"
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        user = ImagerProfile.objects.filter(user=current_user).first()
        userdata = {'username': user.user,
                    'location': (user.city + ', ' + user.state),
                    'pic': user.pic,
                    'job': user.job,
                    'camera': user.camera_type,
                    'photostyle': user.photography_style,
                    'website': user.website,
                    'pub_pics': user.pub_pics,
                    'pub_albums': user.pub_albums,
                    'prv_pics': user.prv_pics,
                    'prv_albums': user.prv_albums,
                    }
        return userdata


class LibraryView(ListView):
    template_name = 'imagersite/library.html'
    model = ImagerPhoto

    def get_context_data(self, **kwargs):
        photos = ImagerPhoto.objects.all()
        return {'photos': photos}
