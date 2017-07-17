"""Test file for the images app."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import factory
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = settings.MEDIA_ROOT
media = os.path.join(MEDIA_ROOT)
os.system('mv ' + media + '/cache/ ' + media + '/cache_real//')


class UserFactory(factory.django.DjangoModelFactory):
    """Generate users for testing."""

    class Meta:
        """Meta info."""

        model = User

    username = factory.Sequence(lambda n: "User number {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@example.com".format(x.username.replace(" ", ""))
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    """Generate photos for testing."""

    class Meta:
        """Meta info."""

        model = ImagerPhoto

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Photo number {}".format(n))
    description = factory.LazyAttribute(
        lambda a: '{} is confirmed a photo'.format(a.title))
    photo = SimpleUploadedFile(
        name='sample.jpg',
        content=open(os.path.join(BASE_DIR,
                                  'static',
                                  'random_def.jpg'
                                  ), 'rb').read(),
        content_type='image/jpeg'
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Generate albums for testing."""

    class Meta:
        """Meta info."""

        model = ImagerAlbum

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Album number {}".format(n))
    description = factory.LazyAttribute(
        lambda a: '{} is confirmed an album'.format(a.title))


class PhotoTestCase(TestCase):
    """Photo tests for view and model."""

    def setUp(self):
        """Set up users and photos for testing.."""
        self.user = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]

    def tearDown(self):
        """Teardown when tests complete."""
        images_del = os.path.join(MEDIA_ROOT, 'images', 'sample*.jpg')
        os.system('rm -rf ' + images_del)
        os.system('rm -rf ' + media + '/cache/')

    def test_photo_made_when_saved(self):
        """Test photos are added to the database."""
        self.assertTrue(ImagerPhoto.objects.count() == 20)

    def test_photo_associated_with_user(self):
        """Test that a photo is attached to a user."""
        photo = ImagerPhoto.objects.first()
        self.assertTrue(hasattr(photo, "__str__"))

    def test_photo_has_str(self):
        """Test photo model includes a string for user."""
        photo = ImagerPhoto.objects.first()
        self.assertTrue(hasattr(photo, "user"))

    def test_image_has_been_published(self):
        """Test that the image is published privately."""
        image = ImagerPhoto.objects.first()
        image.published = 'PV'
        image.save()
        self.assertTrue(ImagerPhoto.objects.first().published == "PV")
        self.tearDown()


class AlbumTestCase(TestCase):
    """Album tests for model and view."""

    def setUp(self):
        """Set up album with photos, users, and albums."""
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.albums = [AlbumFactory.create() for i in range(20)]

    def tearDown(self):
        """Teardown when tests complete."""
        images_del = os.path.join(MEDIA_ROOT, 'images', 'sample*.jpg')
        os.system('rm -rf ' + images_del)
        os.system('rm -rf ' + media + '/cache/')

    def test_image_no_album(self):
        """Test that the image is not in an album."""
        image = ImagerPhoto.objects.first()
        self.assertTrue(image.albums.count() == 0)

    def test_image_has_album(self):
        """Test that the image is in an album."""
        image = ImagerPhoto.objects.first()
        album = ImagerAlbum.objects.first()
        image.albums.add(album)
        self.assertTrue(image.albums.count() == 1)

    def test_album_has_no_image_inside(self):
        """Test that an album has no image inside of it."""
        album = ImagerAlbum.objects.first()
        self.assertTrue(album.photos.count() == 0)

    def test_album_has_image_inside(self):
        """Test that an album has an image inside of it."""
        image = ImagerPhoto.objects.first()
        album = ImagerAlbum.objects.first()
        image.albums.add(album)
        self.assertTrue(image.albums.count() == 1)
        self.tearDown()


class LibraryTestCase(TestCase):
    """Test library view has photos and albums."""

    def setUp(self):
        """Setup."""
        self.client = Client()
        self.user = User(username='deckardcain',
                         email='deck@rd.cain')
        self.user.set_password('secret')
        self.user.save()

        self.photos = [PhotoFactory.create() for i in range(20)]
        self.album = AlbumFactory.create()
        photos = ImagerPhoto.objects.all()
        album = ImagerAlbum.objects.first()
        for photo in photos:
            photo.albums.add(album)
            self.user.photos.add(photo)
        self.user.albums.add(album)
        self.user.save()

    def tearDown(self):
        """Teardown when tests complete."""
        images_del = os.path.join(MEDIA_ROOT, 'images', 'sample*.jpg')
        os.system('rm -rf ' + images_del)
        os.system('rm -rf ' + media + '/cache/')

    def login_helper(self, username, password):
        """Log in using a post request."""
        return self.client.post(reverse_lazy('login'),
                                {'username': username,
                                 'password': password},
                                follow=True)

    def test_library_has_users_content(self):
        """Test that users albums and photos are present."""
        self.login_helper('deckardcain', 'secret')
        response = self.client.get(reverse_lazy('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(21, len(html.findAll('h6')))
        self.assertTrue(html.find('img', {'src': '/static/black.png'}))

    def test_individual_image_page_contents(self):
        """Test that the single photo page has content."""
        self.login_helper('deckardcain', 'secret')
        pic_id = ImagerPhoto.objects.first().id
        response = self.client.get(reverse_lazy('photo',
                                                kwargs={'photo_id': pic_id}))
        self.assertTrue(b'photo-page' in response.content)

    def test_individual_album_page_contents(self):
        """Test that the single album page has content."""
        self.login_helper('deckardcain', 'secret')
        alb_id = ImagerAlbum.objects.first().id
        response = self.client.get(reverse_lazy('album',
                                                kwargs={'album_id': alb_id}))
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(20, len(html.findAll('h6')))
        self.tearDown()
