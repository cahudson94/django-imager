"""View file for django imagerproject."""
from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader


def home_view(request):
    """Home view for imager."""
    context = {'bobs': 'groot'}
    return render(request, 'imagersite/home.html', context=context)


def account_view(request):
    """Registration view for imager."""
    return render(request, 'imagersite/registration_form.html')
