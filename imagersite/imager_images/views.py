"""View file for all image related pages."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from imager_images.models import ImagerPhoto, ImagerAlbum
from imager_images.forms import PhotoForm, AlbumForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


class LibraryView(LoginRequiredMixin, TemplateView):
    """"List view for albums and photos."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(LibraryView, self).get_context_data(**kwargs)
        request = context['view'].request
        photo_list = ImagerPhoto.objects.filter(user=request.user)
        album_list = ImagerAlbum.objects.filter(user=request.user)
        photo_paginator = Paginator(photo_list, 4)
        album_paginator = Paginator(album_list, 4)
        if 'album_page' in request.GET:
            album_page = request.GET.get('album_page').split('?photo_page=')[0]
            photo_page = request.GET.get('album_page').split('?photo_page=')[1]
        else:
            album_page = 1
            photo_page = 1
        try:
            context['photos'] = photo_paginator.page(photo_page)
        except PageNotAnInteger:
            context['photos'] = photo_paginator.page(1)
        except EmptyPage:
            context['photos'] = photo_paginator.page(photo_paginator.num_pages)
        try:
            context['albums'] = album_paginator.page(album_page)
        except PageNotAnInteger:
            context['albums'] = album_paginator.page(1)
        except EmptyPage:
            context['albums'] = album_paginator.page(album_paginator.num_pages)
        context['photo_tags'] = set([tag for photo in context['photos'] for tag in photo.tags.names()])
        context['album_tags'] = set([tag for album in context['albums'] for tag in album.tags.names()])
        return context


class PhotosView(TemplateView):
    """"List view for albums and photos."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(PhotosView, self).get_context_data(**kwargs)
        request = context['view'].request
        photo_list = ImagerPhoto.objects.filter(user=request.user)
        photo_paginator = Paginator(photo_list, 4)
        album_paginator = Paginator([], 4)
        if 'album_page' in request.GET:
            photo_page = request.GET.get('album_page').split('?photo_page=')[1]
        else:
            photo_page = 1
        try:
            context['photos'] = photo_paginator.page(photo_page)
        except PageNotAnInteger:
            context['photos'] = photo_paginator.page(1)
        except EmptyPage:
            context['photos'] = photo_paginator.page(photo_paginator.num_pages)
        context['albums'] = album_paginator.page(album_paginator.num_pages)
        context['photo_tags'] = set([tag for photo in context['photos'] for tag in photo.tags.names()])
        return context


class AlbumsView(TemplateView):
    """"List view for albums and photos."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(AlbumsView, self).get_context_data(**kwargs)
        request = context['view'].request
        album_list = ImagerAlbum.objects.filter(user=request.user)
        photo_paginator = Paginator([], 4)
        album_paginator = Paginator(album_list, 4)
        if 'album_page' in request.GET:
            album_page = request.GET.get('album_page').split('?photo_page=')[0]
        else:
            album_page = 1
        context['photos'] = photo_paginator.page(photo_paginator.num_pages)
        try:
            context['albums'] = album_paginator.page(album_page)
        except PageNotAnInteger:
            context['albums'] = album_paginator.page(1)
        except EmptyPage:
            context['albums'] = album_paginator.page(album_paginator.num_pages)
        context['album_tags'] = set([tag for album in context['albums'] for tag in album.tags.names()])
        return context


class SinglePhotoView(LoginRequiredMixin, DetailView):
    """The view for individual photos."""

    template_name = 'imager_images/photo.html'
    model = ImagerPhoto

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(SinglePhotoView, self).get_context_data(**kwargs)
        context['photo'] = context['imagerphoto']
        user = context['view'].request.user
        tags = set(context['photo'].tags.names())
        shared_tags = (ImagerPhoto.objects.filter(user=user)
                                          .filter(tags__name__in=tags).distinct())
        num = 5 if len(shared_tags) >= 5 else len(shared_tags)
        shared_sample = random.sample(list(shared_tags), num)
        context['shared_tags'] = set(photo for photo in shared_sample)
        return context


class SingleAlbumView(LoginRequiredMixin, DetailView):
    """The view for individual albums."""

    template_name = 'imager_images/album.html'
    model = ImagerAlbum

    def get_context_data(self, **kwargs):
        """Provide context for the view."""
        context = super(SingleAlbumView, self).get_context_data(**kwargs)
        request = context['view'].request
        context['album'] = context['imageralbum']
        photos = context['imageralbum'].photos.all()
        paginator = Paginator(photos, 4)
        page = request.GET.get('page')
        try:
            context['photos'] = paginator.page(page)
        except PageNotAnInteger:
            context['photos'] = paginator.page(1)
        except EmptyPage:
            context['photos'] = paginator.page(paginator.num_pages)
        context['photo_tags'] = set([tag for photo in context['photos'] for tag in photo.tags.names()])
        context['album_tags'] = set([tag for tag in context['album'].tags.names()])
        return context


class PhotoCreate(LoginRequiredMixin, CreateView):
    """View to create a new photo."""

    template_name = 'imager_images/add_photo.html'
    model = ImagerPhoto
    form_class = PhotoForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Tie form data to user."""
        form.instance.user = self.request.user
        return super(CreateView, self).form_valid(form)


class PhotoEdit(LoginRequiredMixin, UpdateView):
    """View to edit an existing photo."""

    template_name = 'imager_images/edit_photo.html'
    model = ImagerPhoto
    form_class = PhotoForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Tie form data to user."""
        form.instance.user = self.request.user
        return super(UpdateView, self).form_valid(form)


class AlbumCreate(LoginRequiredMixin, CreateView):
    """Add an album instance."""

    template_name = 'imager_images/add_album.html'
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
        return super(CreateView, self).form_valid(form)


class AlbumEdit(LoginRequiredMixin, UpdateView):
    """Edit an album instance."""

    template_name = 'imager_images/edit_album.html'
    model = ImagerAlbum
    form_class = AlbumForm
    success_url = reverse_lazy('library')

    def get_form(self):
        """Prepopulate form fields."""
        form = super(AlbumEdit, self).get_form()
        photos = ImagerPhoto.objects.filter(user=self.request.user)
        form.fields['photos'].queryset = photos
        form.fields['cover'].queryset = photos
        return form

    def form_valid(self, form):
        """Tie form data to user."""
        form.instance.user = self.request.user
        return super(UpdateView, self).form_valid(form)


class AlbumTagListView(ListView):
    """The list of albums with a given tag."""

    template_name = 'imager_images/tagged_albums.html'

    def get_queryset(self):
        """Filter for the tag."""
        return(ImagerAlbum.objects.filter(user=self.request.user)
                                  .filter(tags__name__in=self.kwargs.get('slug')))

    def get_context_data(self, **kwargs):
        """Return the requested albums."""
        context = super(AlbumTagListView, self).get_context_data(**kwargs)
        request = context['view'].request
        context['tag'] = self.kwargs.get('slug')
        albums = (ImagerAlbum.objects.filter(user=self.request.user)
                                     .filter(tags__name__in=[self.kwargs.get('slug')]).all())
        paginator = Paginator(albums, 4)
        page = request.GET.get('page')
        try:
            context['albums'] = paginator.page(page)
        except PageNotAnInteger:
            context['albums'] = paginator.page(1)
        except EmptyPage:
            context['albums'] = paginator.page(paginator.num_pages)
        return context


class PhotoTagListView(ListView):
    """The list of photos with a given tag."""

    template_name = 'imager_images/tagged_photos.html'

    def get_queryset(self):
        """Filter for the tag."""
        return(ImagerPhoto.objects.filter(user=self.request.user)
                                  .filter(tags__slug=[self.kwargs.get('slug')]).all())

    def get_context_data(self, **kwargs):
        """Return the requested photos."""
        context = super(PhotoTagListView, self).get_context_data(**kwargs)
        request = context['view'].request
        context['tag'] = self.kwargs.get('slug')
        photos = (ImagerPhoto.objects.filter(user=self.request.user)
                                     .filter(tags__name__in=[self.kwargs.get('slug')]).all())
        paginator = Paginator(photos, 4)
        page = request.GET.get('page')
        try:
            context['photos'] = paginator.page(page)
        except PageNotAnInteger:
            context['photos'] = paginator.page(1)
        except EmptyPage:
            context['photos'] = paginator.page(paginator.num_pages)
        return context
