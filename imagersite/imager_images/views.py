from django.views.generic.edit import CreateView
from imager_images.models import ImagerPhoto


class ImageCreate(CreateView):
    model = ImagerPhoto
    fields = ['photo', 'description', 'title', 'user', 'published', 'date_published']
    template_name = "imager_images/imagerphoto_form.html"
