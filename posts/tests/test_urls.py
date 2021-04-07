from django.test import Client, TestCase

from posts.models import Group, Post, User


class GeneralURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(username='TestUser')
        cls.user2 = User.objects.create(username='TestUser2')
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
        cls.post2 = Post.objects.create(
            text='Тестовый текст',
            author=cls.user2,
            group=cls.group
        )

    def test_urls_guest_client(self):
        urls = {
            '/': 200,
            f'/group/{GeneralURLTests.group.slug}/': 200,
            '/new/': 302,
            f'/{GeneralURLTests.post.author}/': 200,
            f'/{GeneralURLTests.post.author}/{GeneralURLTests.post.id}/': 200,
            (f'/{GeneralURLTests.post.author}/'
             f'{GeneralURLTests.post.id}/edit/'): 302
        }
        for url, expected_status in urls.items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_authorized_client(self):
        urls = {
            '/': 200,
            f'/group/{GeneralURLTests.group.slug}/': 200,
            '/new/': 200,
            f'/{GeneralURLTests.post.author}/': 200,
            f'/{GeneralURLTests.post.author}/{GeneralURLTests.post.id}/': 200
        }
        for url, expected_status in urls.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_authorized_client_author(self):
        urls = {
            (f'/{GeneralURLTests.post.author}/'
             f'{GeneralURLTests.post.id}/edit/'): 200
        }
        for url, expected_status in urls.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_authorized_client_not_author_redirect(self):
        urls = {
            (f'/{GeneralURLTests.post2.author}/'
             f'{GeneralURLTests.post2.id}/edit/'): 302
        }
        for url, expected_status in urls.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'index.html': '/',
            'group.html': f'/group/{GeneralURLTests.group.slug}/',
            'new_post.html': '/new/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_use_correct_template(self):
        response = self.authorized_client.get(
            f'/{GeneralURLTests.post.author}/{GeneralURLTests.post.id}/edit/'
        )
        self.assertTemplateUsed(response, 'new_post.html')
