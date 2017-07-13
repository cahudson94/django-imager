"""View file for django imagerproject."""
from django.shortcuts import render
from imager_profile.models import ImagerProfile
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.contrib.auth.models import User


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


def user_profile_view(request, request_username):
    """The view for another users profile."""
    user = request_username.lower()
    request_user = User.objects.filter(username=user)
    profile = ImagerProfile.objects.filter(user=request_user)
    pub_pics = (ImagerPhoto.objects
                .filter(user=request_user)
                .filter(published='PB'))
    pub_albums = (ImagerAlbum.objects
                  .filter(user=request_user)
                  .filter(published='PB'))
    return render(
        request,
        'imagersite/other_profile.html',
        context={
            'user': user,
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


def library_view(request):
    """The view for the user galleries."""
    photos = ImagerPhoto.objects.all()
    albums = ImagerAlbum.objects.all()
    return render(request, 'imagersite/library.html',
                  {'photos': photos,
                   'albums': albums})

def photo_view(request):
    """The view for individual photos."""
    photo = ImagerPhoto.objects.query()



def album_view(request):
    """The view for individual photos."""