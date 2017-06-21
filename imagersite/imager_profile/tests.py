"""Tests for imager profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.urls import reverse

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

    def test_profile_has_correct_attrs(self):
        """Test that correct attributes are on profile."""
        self.assertTrue(ImagerProfile.objects.first().photography_style, 'Color')
        self.assertTrue(ImagerProfile.objects.first().active, False)

    def test_deletion_of_lives(self):
        """Delete that user, reduce user count."""
        print(User.objects.all())
        user = User.objects.filter(username='user50')
        user.delete()
        print(self.users)
        self.assertEquals(24, len(ImagerProfile.objects.all()))

    def test_add_attr_and_check_if_true(self):
        """Add attributes and check that everything is added and true."""
        ImagerProfile.objects.first().job = 'Dinosaur wrangler'
        ImagerProfile.objects.first().website = 'raptorrider.com'
        ImagerProfile.objects.first().camera_type = 'Canon'
        ImagerProfile.objects.first().photography_style = 'Landscape'
        ImagerProfile().save()
        self.assertTrue(ImagerProfile.objects.first().job, 'Dinosaur wrangler')
        self.assertTrue(ImagerProfile.objects.first().website, 'raptorrider.com')
        self.assertTrue(ImagerProfile.objects.first().camera_type, 'Canon')
        self.assertTrue(ImagerProfile.objects.first().photography_style, 'Landscape')
