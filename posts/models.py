from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы:',
        help_text='Введите название группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес страницы:',
        help_text='Введите адрес странницы'
    )
    description = models.TextField(
        verbose_name='Описание группы:',
        help_text='Введите описание группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст:',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа:',
        help_text='Выберите группу (необязательно)'
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
