from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, unique=True,
        help_text='Название подборки',
        verbose_name='Название подборки'
    )
    slug = models.SlugField(
        unique=True,
        help_text='Часть адресной строки для подборки',
        verbose_name='SLUG'
    )
    description = models.TextField(
        verbose_name='Описание подборки'
    )

    class Meta:
        verbose_name = 'Подборка записей'
        verbose_name_plural = 'Подборки записей'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст записи'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts', verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='posts', verbose_name='Подборка записей'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.text[:15]
