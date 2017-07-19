"""View file for django imagerproject."""
from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.contrib.auth.models import User
from random import randint
import datetime


def home_view(request):
    """Home view for imager."""
    current_user = request.user
    photos = ImagerPhoto.objects.all().filter(published='PB')
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
    context = {'user': current_user,
               'random_photo': random_photo,
               'title': title,
               'description': description,
               'date': date_uploaded,
               'random_user': user}
    return render(request, 'imagersite/home.html', context=context)


def profile_view(request):
    """The view for our profile page."""
    current_user = request.user
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
    userdata = {'username': user.user,
                'location': (user.city + ', ' + user.state),
                'pic': user.pic,
                'job': user.job,
                'camera': user.camera_type,
                'photostyle': user.photography_style,
                'website': user.website,
                'pub_pics': pub_pics,
                'pub_albums': pub_albums,
                'prv_pics': prv_pics,
                'prv_albums': prv_albums,
                }
    return render(request, 'imagersite/profile.html', context=userdata)


def user_profile_view(request, request_username=None):
    """The view for another users profile."""
    user = request.user
    request_username = request_username.lower()
    request_user = User.objects.get(username=request_username)
    profile = ImagerProfile.objects.get(user=request_user)
    pub_pics = (ImagerPhoto.objects
                .filter(user=request_user)
                .filter(published='PB')).count()
    pub_albums = (ImagerAlbum.objects
                  .filter(user=request_user)
                  .filter(published='PB')).count()
    return render(
        request,
        'imagersite/other_profile.html',
        context={
            'user': user,
            'requested_user': request_username,
            'username': profile.user,
            'location': (profile.city + ', ' + profile.state),
            'pic': profile.pic,
            'job': profile.job,
            'camera': profile.camera_type,
            'photostyle': profile.photography_style,
            'website': profile.website,
            'pub_pics': pub_pics,
            'pub_albums': pub_albums,
        }
    )
