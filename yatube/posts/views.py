from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

PAGINATOR_COUNT_PER_PAGE: int = 10

def pagination(request, objects, num_per_page):
    """Рутина подготовки Пагинатора для страниц.
    
    аргументы:
    request - HttpRequest от запрошенной страницы, содержит номер страницы,
              для которой нужно вывести порцию объектов
    objects - перечень объектов, которые надо разбить постранично
    num_per_page - сколько объектов выводить на странице
    return - порция объектов для номера страницы из request
    """
    paginator = Paginator(objects, num_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

def index(request):
    post_list = Post.objects.all()
    page = pagination(request, post_list, PAGINATOR_COUNT_PER_PAGE)
    return render(
        request,
        'posts/index.html',
        {'page': page},
    )

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()    
    page = pagination(request, posts, PAGINATOR_COUNT_PER_PAGE)

    return render(request, 'posts/group.html', {'group': group, 'page': page})


def group_index(request):
    groups = Group.objects.all()
    page = pagination(request, groups, PAGINATOR_COUNT_PER_PAGE)
    return render(request, 'posts/group_index.html',
                  {'groups': groups, 'page': page})


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

    return render(request, 'posts/new_post.html',
                  {'form': form, 'edit_flag': False})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    user_posts = profile_user.posts.all()
    page = pagination(request, objeuser_postscts, PAGINATOR_COUNT_PER_PAGE)

    return render(request, 'posts/profile.html',
                  {'profile_user': profile_user,
                   'page': page})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(
        request, 'posts/post.html',
        {'post': post, 'username': username,
         'author': post.author, 'post_id': post_id}
    )

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.username == post.author.username:
        if request.method != 'POST':
            form = PostForm(instance=post)
        else:
            form = PostForm(instance=post, data=request.POST)

            if form.is_valid():
                post.save()
                return redirect('post', username=username, post_id=post_id)
        return render(
            request, 'posts/new_post.html',
            {'form': form, 'post': post,
             'edit_flag': True, 'username': username,
             'author': post.author, 'post_id': post_id}
        )
    return redirect('post', username=username, post_id=post_id)
