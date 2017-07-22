"""."""
from django.shortcuts import render
from imager_images.models import ImagerAlbum, ImagerPhoto


def library_view(request):
    """The view for the user galleries."""
    user = request.user
    photos = ImagerPhoto.objects.filter(user=user)
    albums = ImagerAlbum.objects.filter(user=user)
    return render(request, 'imagersite/library.html',
                  {'photos': photos,
                   'albums': albums})


def photos_view(request):
    """The view for the user photos."""
    user = request.user
    photos = ImagerPhoto.objects.filter(user=user)
    return render(request, 'imagersite/library.html',
                  {'photos': photos})


def albums_view(request):
    """The view for the user albums."""
    user = request.user
    albums = ImagerAlbum.objects.filter(user=user)
    return render(request, 'imagersite/library.html',
                  {'albums': albums})


def photo_view(request, pk):
    """The view for individual photos."""
    photo = ImagerPhoto.objects.get(id=pk)
    return render(
        request,
        'imagersite/photo.html',
        context={'photo': photo})


def album_view(request, pk):
    """The view for individual photos."""
    album = ImagerAlbum.objects.get(id=pk)
    photos = album.photos.all()
    return render(
        request,
        'imagersite/album.html',
        context={'album': album, 'photos': photos})
