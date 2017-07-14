"""Test file for the images app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import ImagerPhoto, ImagerAlbum
import factory


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


class AlbumTestCase(TestCase):
    """Album tests for model and view."""

    def setUp(self):
        """Set up album with photos, users, and albums."""
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.albums = [AlbumFactory.create() for i in range(20)]

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
