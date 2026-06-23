from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Post, Category, Tag

User = get_user_model()


class BlogSmokeTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            password='pass'
        )
        self.cat = Category.objects.create(name='TestCat')

    def test_home_status(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_post_creation_and_detail(self):
        post = Post.objects.create(
            title='T1',
            content='Hello',
            author=self.user,
            category=self.cat,
            status='published',
            published_at=timezone.now()
        )

        resp = self.client.get(
            reverse('post_detail', kwargs={'slug': post.slug})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'T1')

    def test_like_toggle(self):
        post = Post.objects.create(
            title='LikeMe',
            content='Hi',
            author=self.user,
            category=self.cat,
            status='published',
            published_at=timezone.now()
        )

        self.client.login(username='tester', password='pass')

        resp = self.client.post(
            reverse('post_like', kwargs={'slug': post.slug})
        )
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(post.likes.count(), 1)

        # Toggle off
        self.client.post(reverse('post_like', kwargs={'slug': post.slug}))
        self.assertEqual(post.likes.count(), 0)

    def test_home_renders_tagcloud(self):
        t1 = Tag.objects.create(name='alpha')
        t2 = Tag.objects.create(name='beta')

        post = Post.objects.create(
            title='Tagged',
            content='Has tags',
            author=self.user,
            category=self.cat,
            status='published',
            published_at=timezone.now()
        )

        post.tags.add(t1, t2)

        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'alpha')
        self.assertContains(resp, 'beta')