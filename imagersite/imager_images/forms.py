"""Form file for addition and editing."""
from django import forms
from imager_images.models import ImagerPhoto, ImagerAlbum


class PhotoForm(forms.ModelForm):
    """Form for photo addition."""

    class Meta:
        """."""

        model = ImagerPhoto
        fields = ['title', 'description', 'published', 'photo']
        widgets = {
            'description': forms.Textarea()
        }


class AlbumForm(forms.ModelForm):
    """Form for album addition."""

    class Meta:
        """."""

        model = ImagerAlbum
        exclude = ['user', 'date_published']
        widgets = {
            'description': forms.Textarea()
        }
