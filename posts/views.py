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
    context = {
        'page': page
    }
    return render(
        request,
        'index.html',
        context
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page': page
    }
    return render(
        request,
        'group.html',
        context
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    context = {
        'form': form
    }
    return render(
        request,
        'new_post.html',
        context
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'page': page,
    }
    return render(
        request,
        'profile.html',
        context
    )


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'author': author,
        'post': post
    }
    return render(
        request,
        'post.html',
        context
    )


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect(
            'post',
            username=username,
            post_id=post_id
        )
    form = PostForm(request.POST or None, instance=post)
    if request.user == post.author and form.is_valid():
        form.save()
        return redirect(
            'post',
            username=username,
            post_id=post_id
        )
    context = {
        'author': author,
        'post': post,
        'form': PostForm(instance=post),
    }
    return render(
        request,
        'new_post.html',
        context
    )
