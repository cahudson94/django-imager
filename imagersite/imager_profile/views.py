"""View file for django imagerproject."""
from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto
# from django.http import HttpResponse
# from django.template import loader


def home_view(request):
    """Home view for imager."""
    context = {'bobs': 'groot'}
    return render(request, 'imagersite/home.html', context=context)


def account_view(request):
    """Registration view for imager."""
    return render(request, 'imagersite/accounts.html')


def profile_view(request):
    """The view for our profile page."""
    current_user = request.user
    user = ImagerProfile.objects.filter(user=current_user).first()
    userdata = {'username': user.user,
                'job': user.job,
                'camera': user.camera_type,
                'photostyle': user.photography_style,
                'website': user.website
                }
    return render(request, 'imagersite/profile.html', context=userdata)


def gallery_view(request):
    """The view for the user galleries."""
    photos = ImagerPhoto.objects.all()
    return render(request, 'imagersite/gallery.html', {'photos': photos})
