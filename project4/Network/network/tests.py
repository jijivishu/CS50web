from django.test import TestCase
from .models import User, Post, Like, Follow

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):

        # Create user
        test_user_1 = User.objects.create(email="a@b.com", username="test_user_1", password="1234", confirmation="1234")
        test_user_2 = User.objects.create(email="a@b.com", username="test_user_2", password="1234", confirmation="1234")

        # Create posts
        test_post_1 = Post.objects.create(owner=test_user_1, content="Test Post 1 by User 1", image="")
        test_post_2 = Post.objects.create(owner=test_user_2, content="Test Post 2 by User 2")
        test_post_3 = Post.objects.create(owner=test_user_1, )
        test_post_4 = Post.objects.create()

        # Like posts
        Like.objects.create(liker=test_user_1, liked=test_post_1)
        Like.objects.create(liker=test_user_1, liked=test_post_2)
        Like.objects.create(liked=test_post_1)
        Like.objects.create(liker=test_user_1)

        # Follow people
        Follow.objects.create(follower=test_user_1, following=test_user_2)
        Follow.objects.create(follower=test_user_1, following=test_user_1)
        Follow.objects.create(following=test_user_2)
        Follow.objects.create(follower=test_user_1)

        # No tests yet
