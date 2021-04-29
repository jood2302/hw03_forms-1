from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


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


@login_required
def new_post(request):
    """Create new post for blog."""

    form = PostForm(request.POST or None)
    # initialise PostForm() with 'None' if request.POST absent

    if request.method == 'POST':

        if form.is_valid():
            new_Post = form.save(commit=False)
            new_Post.author = request.user
            new_Post.save()
            return redirect('index')

    return render(request, 'posts/new_post.html', {'form': form})
