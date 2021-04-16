from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, unique=True,
                             help_text="Title of group.")
    slug = models.SlugField(unique=True,
                            help_text="Short name of Group for URL.")
    description = models.TextField()

    class Meta:
        verbose_name = 'Group of posts'
        verbose_name_plural = 'Groups of posts'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='posts')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)
