import datetime as dt

from django.shortcuts import get_object_or_404, render, redirect

from .models import Group, Post
from .forms import PostForm


def index(request):
    latest = Post.objects.all()[:11]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


def group_index(request):
    groups = Group.objects.all()
    return render(request, 'posts/group_index.html', {'groups': groups})


def new_post(request):
    """Create new post for blog."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_Post = Post()
            new_Post.text = form.cleaned_data['text']
            new_Post.author = request.user
            new_Post.group = form.cleaned_data['group']
            new_Post.pub_date = dt.date.today()
            new_Post.save_base()
            return redirect('index')
        return render(request, 'posts/new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})
