"""Tests for imager profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.urls import reverse_lazy
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Make fake users."""

    class Meta:
        """Set fake users name and email."""

        model = User
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.Sequence(
        lambda n: 'user{}@cookies.com'.format(n)
    )


class ProfileTestCase(TestCase):
    """Testing starts here... for the model at least."""

    def setUp(self):
        """Create the fake users."""
        users = [UserFactory.create() for i in range(25)]

        for user in users:
            user.set_password('cake')
            user.save()

        self.users = users

    def test_users_have_profiles_raises_an_exception(self):
        """The function says it all."""
        with self.assertRaises(Exception):
            profile = ImagerProfile()
            profile.save()

    def test_users_profile_are_equal(self):
        """Test that when a user is created it has a profile."""
        self.assertEquals(len(self.users), len(ImagerProfile.objects.all()))

    def test_correct_amount_of_profiles(self):
        """Test amount of profiles."""
        self.assertEquals(25, len(ImagerProfile.objects.all()))

    def test_profile_is_associated_with_actual_users(self):
        """Test profile is associated with actual users."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_profile_has_correct_attrs(self):
        """Test that correct attributes are on profile."""
        self.assertTrue(
            ImagerProfile.objects.first().photography_style, 'Color')
        self.assertTrue(ImagerProfile.objects.first().active, False)


class LoginTestCase(TestCase):
    """Our login and register tests."""

    def login_helper(self, username, password):
        """Log in using a post request."""
        return self.client.post('/login', {'username': username,
                                           'password': password})

    def test_register(self):
        """Test registration is available, and redirects on post."""
        username = 'dino'
        email = 'dino@dino.com'
        password = 'secretpass'
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/accounts/register/', ({
            'username': username,
            'email': email,
            'password': password
        }))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Test login is reachable when not logged in.

        login changes auth.
        """
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        deckardcain = UserFactory(username='deckardcain', password='secret')
        self.login_helper('deckardcain', 'secret')
        assert deckardcain.is_authenticated()

    def test_profile_view_redirect(self):
        """Unauthenticated user redirected when trying.

        to view personal profile.
        """
        response = self.client.get('/logout/', follow=False)
        self.assertEqual(response.status_code, 302)
