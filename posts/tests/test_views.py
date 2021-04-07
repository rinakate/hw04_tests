from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class GeneralModelTest(TestCase):
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

    def test_pages_use_correct_template(self):
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': reverse('group', kwargs={'slug': 'test_slug'}),
            'new_post.html': reverse('new_post')
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['page'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_author_0, 'TestUser')

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'test_slug'})
        )
        self.assertEqual(
            response.context['group'].title, 'Тестовое название'
        )
        self.assertEqual(
            response.context['group'].slug, 'test_slug'
        )
        self.assertEqual(
            response.context['group'].description, 'Тестовое описание'
        )

    def test_new_post_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('post_edit', kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            })
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertEqual(
            response.context['author'], self.user
        )
        self.assertEqual(
            response.context['page'][0], self.post
        )

    def test_post_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('post', kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            })
        )
        context = {
            response.context['post'].text: 'Тестовый текст',
            response.context['post'].author.username: self.user.username
        }
        for key, value in context.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(key, value)

    def test_post_on_index(self):
        response = self.authorized_client.get(reverse('index'))
        precount = len(response.context['page'])
        test_post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group
        )
        response = self.authorized_client.get(reverse('index'))
        postcount = len(response.context['page'])
        new_post = response.context['page'].object_list[0]
        self.assertEqual(precount + 1, postcount)
        self.assertEqual(test_post, new_post)

    def test_post_on_group(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'test_slug'})
        )
        test_post = response.context['page'].object_list[0]
        self.assertEqual(self.post, test_post)

    def test_post_not_on_another_group(self):
        another_group = Group.objects.create(
            title='Тестовое название 2',
            slug='test_slug_2',
            description='Тестовое описание'
        )
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'test_slug_2'})
        )
        another_posts = response.context['page']
        self.assertNotIn(self.post, another_posts)
