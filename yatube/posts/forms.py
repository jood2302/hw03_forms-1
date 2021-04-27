from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'text' : 'Введите текст записи', 'group' : 'Выберите подборку',}
        help_texts = {'text' : 'Что-то стоящее', 'group' : 'Из уже существующих',}
