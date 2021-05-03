from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'posts/index.html',
        {'page': page},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/group.html', {'group': group, 'page': page})


def group_index(request):
    groups = Group.objects.all()
    return render(request, 'posts/group_index.html', {'groups': groups})


@login_required
def new_post(request):
    """For post-obj create form, render and check it, then save model-obj."""

    # initialise PostForm() with 'None' if request.POST absent
    form = PostForm(request.POST or None)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')

    return render(request, 'posts/new_post.html', {'form': form})

def profile(request, username):
    profile_user = User.objects.get(username=username)

    user_posts = profile_user.posts.all()
    post_count = user_posts.count()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/profile.html',
                  {'profile_user': profile_user,
                   'page': page, 'post_count': post_count})

def post_view(request, username, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post.html', { 'post': post }) 

@login_required
def post_edit(request, username, post_id):
    if request.username == username:
        post = Post.objects.get(id=post_id)
        if request.method != 'POST':
            form = PostForm(instance=post)
            
        else:
            form = PostForm(instance=post, data=request.POST)

            if form.is_valid():
                post.save()
                return redirect('index')
        return render(request, 'posts/new_post.html', {'form': form, 'post': post, 'edit_flag': True})
    

def add_comment(request, username, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post.html', { 'post': post})
