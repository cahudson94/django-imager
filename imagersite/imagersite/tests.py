"""Test file for the urls and views."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from django.conf import settings
import os

media = os.path.join(settings.MEDIA_ROOT)


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
        return self.client.post(reverse_lazy('login'),
                                {'username': username,
                                 'password': password})

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
        os.system('mv ' + media + '/cache_real/ ' + media + '/cache/')
