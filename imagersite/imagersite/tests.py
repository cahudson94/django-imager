"""Test file for the urls and views."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import ImagerPhoto, ImagerAlbum
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
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


class HomePageTests(TestCase):
    """Test the content of the homepage."""

    def setUp(self):
        """Setup."""
        self.client = Client()
        self.user = User(username='cookiemonster',
                         email='cookie@cookie.cookie')
        self.user.set_password('COOKIE')
        self.user.save()

    def login_helper(self, username, password):
        """Log in using a post request."""
        return self.client.post('/login/', {'username': username, 'password': password})

    def test_home_ok(self):
        """Test that home page is available to logged out user."""
        resp = self.client.get(reverse_lazy('home'))
        self.assertEqual(resp.status_code, 200)

    def test_home_has_placeholder_img(self):
        """Test that the home page has the placeholder random image."""
        resp = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(resp.content, 'html.parser')
        self.assertTrue(html.find('img', {'src': '/static/random_def.jpg'}))

    def test_home_page_no_logout_when_not_logged_in(self):
        """Test logout not on homepage."""
        response = self.client.get(reverse_lazy('home'))
        self.assertFalse('logout' in response.content.decode())

    def test_no_reg_button_when_logged_in(self):
        """Registration button dissapears on login."""
        self.login_helper('cookiemonster', 'COOKIE')
        response = self.client.get(reverse_lazy('home'))
        self.assertFalse('Register' in response.content.decode())
        self.assertFalse('Login' in response.content.decode())

    def test_login_has_form(self):
        """Test login has a form."""
        response = self.client.get("/login/")
        self.assertTrue('form' in response.rendered_content)


# class SinglePhotoTestCase(TestCase):
#     """Test for single photo view."""

#     def setUp(self):
#         """Set up users and photos for testing.."""
#         self.user = UserFactory.create()
#         self.photo = PhotoFactory.create()
#         self.client = Client()

#     def test_one_image_on_page(self):
#         """Test that the page has one image."""
#         resp = self.client.get(reverse_lazy('photo'))


# class SingleAlbumTestCase(TestCase):
#     """Test for single abum view."""l
