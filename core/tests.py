from django.test import TestCase
from .models import Profile, Posts
from django.contrib.auth.models import User


# Create your tests here.
class TestProfileClass(TestCase):
    """
    Test class to test profile class properties
    """

    def setUp(self) -> None:
        self.new_user = User(username="user")
        self.new_profile = Profile(user=self.new_user, bio='software developer')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_profile(self):
        self.new_profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        self.new_profile.save_profile()
        profiles = Profile.objects.all()

        self.new_profile.delete_profile()
        self.assertTrue(len(profiles) < 1)


class TestPostsClass(TestCase):
    """
    Test class to test profile class properties
    """

    def setUp(self) -> None:
        self.new_user = User(username="user")
        self.new_post = Posts(user=self.new_user, name='Delani', description='cool', link='www.go.com',
                              image1='img.jpg', image2='img2.jpg', image3='img3.jpg')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Posts))

    def test_save_post(self):
        self.new_post.save_post()
        posts = Posts.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_post(self):
        self.new_post.delete_post()
        posts = Posts.objects.all()

        self.new_post.delete_post()
        self.assertTrue(len(posts) < 1)

