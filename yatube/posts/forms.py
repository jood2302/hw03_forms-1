from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        label = {'text' : 'Введите текст поста', 'group' : 'Выберите группу'}
        help_text = {'text':'Что-то стоящее', 'group':'Из уже существующих'}
