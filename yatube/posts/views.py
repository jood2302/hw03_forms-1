from django.shortcuts import get_object_or_404, render

from .models import Group, Post
from .forms import CreationPost


def index(request):
    latest = Post.objects.all()[:11]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


def group_index(request):
    groups = Group.objects.all()
    return render(request, 'group_index.html', {'groups': groups})


def new_post(request):
    """Create new post for blog.
    
    args:
    returns:
    """
    form = CreationPost()
    # Create new post.
    return render(request, 'new.html', {'form': form})
    
