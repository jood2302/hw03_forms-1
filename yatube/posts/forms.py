from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('text', 'group')
