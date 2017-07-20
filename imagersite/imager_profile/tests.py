"""Tests for imager profile app."""
from django.test import TestCase, Client
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


class ProfileModelTestCase(TestCase):
    """Testing for the profile model least."""

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
            ImagerProfile.objects.first().photo_style, 'Color')
        self.assertTrue(ImagerProfile.objects.first().active, False)


class LoginTestCase(TestCase):
    """Our login and register tests."""

    def setUp(self):
        """Setup."""
        self.client = Client()
        self.user = User(username='deckardcain',
                         email='deck@rd.cain')
        self.user.set_password('secret')
        self.user.save()

    def login_helper(self, username, password):
        """Log in using a post request."""
        return self.client.post(reverse_lazy('login'),
                                {'username': username,
                                 'password': password},
                                follow=True)

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

    def test_login_ok(self):
        """Test login gives 200 response."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_redirects_to_profile(self):
        """Test redirect to profile on proper login."""
        response = self.login_helper('deckardcain', 'secret')
        self.assertTrue(b'<title>Profile</title>' in response.content)

    def test_profile_view_redirect(self):
        """Unauthenticated user redirected when trying.

        to view personal profile.
        """
        response = self.client.get(reverse_lazy('logout'), follow=False)
        self.assertEqual(response.status_code, 302)

    def test_login_has_form(self):
        """Test login has a form."""
        response = self.client.get(reverse_lazy('login'))
        self.assertTrue('form' in response.rendered_content)


class ProfileTestCase(TestCase):
    """Test for user profiles."""

    def setUp(self):
        """Setup."""
        self.client = Client()
        self.user = User(username='deckardcain',
                         email='deck@rd.cain')
        self.user.set_password('secret')
        self.user.save()

    def login_helper(self, username, password):
        """Log in using a post request."""
        return self.client.post(reverse_lazy('login'),
                                {'username': username,
                                 'password': password},
                                follow=True)

    def test_logged_in_user_private_content(self):
        """Test that private counts are visable on user profile."""
        self.login_helper('deckardcain', 'secret')
        response = self.client.get(reverse_lazy('profile'))
        self.assertTrue(b'Private' in response.content)

    def test_public_profile_has_content(self):
        """Test that public profile has public count and 200 ok."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('public_profile',
                                   kwargs={'request_username': 'deckardcain'}))
        self.assertFalse(b'Private' in response.content)
        self.assertTrue(b'Public' in response.content)

    def test_edit_profile_form_contents(self):
        """Test the the edit form has the appropriate fields."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('profile_edit'))
        self.assertTrue(b'deck@rd.cain' in response.content)
        self.assertTrue(b'deckardcain' in response.content)
        self.assertTrue(b'first_name' in response.content)

    def test_edit_redirects_to_profile(self):
        """Test that on submit of form redirects to profile page."""
        self.client.force_login(self.user)
        data = {
            'username': 'deckardcain',
            'email': 'deck@rd.cain',
        }
        response = self.client.post(reverse_lazy('profile_edit'),
                                    data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == reverse_lazy('profile'))

    def test_edit_updates_profile_and_user(self):
        """Test that a submited form updates the changed fields."""
        self.client.force_login(self.user)
        self.assertTrue(self.user.imagerprofile.get_photo_style_display() == 'Color')
        data = {
            'username': 'deckardcain',
            'email': 'deck@rd.cain',
            'first_name': 'deckard',
            'last_name': 'cain',
            'photo_style': 'LS'
        }
        response = self.client.post(reverse_lazy('profile_edit'),
                                    data, follow=True)
        user = User.objects.get(username=self.user.username)
        self.assertTrue(b'Landscape' in response.content)
        self.assertTrue(user.first_name == data['first_name'])
