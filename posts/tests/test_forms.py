from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostsFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовое название',
            slug='test_slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': Group.objects.get(pk=1).pk
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=Group.objects.get(pk=1).pk,
            ).exists()
        )

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Отредактированный тестовый текст',
            'group': Group.objects.get(pk=1).pk
        }
        response = self.authorized_client.post(
            reverse('post_edit', kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('post', kwargs={
                'username': self.post.author.username,
                'post_id': self.post.id
            })
        )
        self.assertEqual(Post.objects.count(), posts_count == posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный тестовый текст',
                group=Group.objects.get(pk=1).pk,
            ).exists()
        )
