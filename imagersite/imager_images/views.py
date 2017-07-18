"""View file for all image related pages."""
from django.views.generic import TemplateView, DeleteView, CreateView
from imager_images.models import ImagerPhoto, ImagerAlbum
from imager_images.forms import PhotoForm, AlbumForm
from django.urls import reverse_lazy


class LibraryView(TemplateView):
    """"List view for albums and photos."""

    template_name = 'imagersite/library.html'

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(LibraryView, self).get_context_data(**kwargs)
        user = context['view'].request.user
        context['photos'] = ImagerPhoto.objects.filter(user=user)
        context['albums'] = ImagerAlbum.objects.filter(user=user)
        return context


class SinglePhotoView(DeleteView):
    """The view for individual photos."""

    template_name = 'imagersite/photo.html'
    model = ImagerPhoto

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(SinglePhotoView, self).get_context_data(**kwargs)
        context['photo'] = context['imagerphoto']
        return context


class SingleAlbumView(DeleteView):
    """The view for individual albums."""

    template_name = 'imagersite/album.html'
    model = ImagerAlbum

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(SingleAlbumView, self).get_context_data(**kwargs)
        context['album'] = context['imageralbum']
        context['photos'] = context['imageralbum'].photos.all()
        return context


class PhotoCreate(CreateView):
    """View to create a new photo."""

    model = ImagerPhoto
    form_class = PhotoForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Tie form data to user."""
        form.instance.user = self.request.user
        return super(CreateView, self).form_valid(form)


class AlbumCreate(CreateView):
    """Add an album instance."""

    model = ImagerAlbum
    form_class = AlbumForm
    success_url = reverse_lazy('library')

    def get_form(self):
        """Prepopulate form fields."""
        form = super(AlbumCreate, self).get_form()
        photos = ImagerPhoto.objects.filter(user=self.request.user)
        form.fields['photos'].queryset = photos
        form.fields['cover'].queryset = photos
        return form

    def form_valid(self, form):
        """Tie form data to user."""
        form.instance.user = self.request.user
        return super(AlbumCreate, self).form_valid(form)
