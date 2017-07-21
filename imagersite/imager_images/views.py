"""."""
from django.shortcuts import render
from imager_images.models import ImagerAlbum, ImagerPhoto


def library_view(request):
    """The view for the user galleries."""
    photos = ImagerPhoto.objects.all()
    albums = ImagerAlbum.objects.all()
    return render(request, 'imagersite/library.html',
                  {'photos': photos,
                   'albums': albums})


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
