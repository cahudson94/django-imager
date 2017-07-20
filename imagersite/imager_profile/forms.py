"""Form file for editing."""
from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    """Form for photo addition."""

    class Meta:
        """."""

        model = User
        fields = []
