from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404


PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()  # type:ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': 'Home'
    }

    return render(
        request,
        'blog/pages/index.html',
        context,
    )


def created_by(request, author_id):
    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404()

    user_full_name = user.username
    posts = (
        Post.objects.get_published().filter(created_by__pk=author_id)  # type:ignore
    )

    if user.first_name:
        user_full_name = f'{user.first_name}'

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': f'Criado por: {user_full_name}'
    }

    return render(
        request,
        'blog/pages/index.html',
        context,
    )


def category(request, slug):
    posts = (
        Post.objects.get_published().filter(category__slug=slug)  # type:ignore
    )

    if len(posts) == 0:
        raise Http404()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': f'Categoria: {page_obj[0].category.name}'
    }

    return render(
        request,
        'blog/pages/index.html',
        context,
    )


def page(request, slug):
    page_obj = (
        Page.objects.filter(
            is_published=True).filter(
            slug=slug).first()  # type:ignore
    )

    if page_obj is None:
        raise Http404()

    context = {
        'page': page_obj,
        'page_title': 'Page'
    }

    return render(
        request,
        'blog/pages/page.html',
        context,
    )


def post(request, slug):
    post_obj = (
        Post.objects.get_published().filter(slug=slug).first()  # type:ignore
    )

    if post_obj is None:
        raise Http404()

    context = {
        'post': post_obj,
        'page_title': 'Post'
    }

    return render(
        request,
        'blog/pages/post.html',
        context,
    )


def tag(request, slug):
    posts = (
        Post.objects.get_published().filter(tags__slug=slug)  # type:ignore
    )

    if len(posts) == 0:
        raise Http404()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': 'Tag',
    }

    return render(
        request,
        'blog/pages/index.html',
        context,
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published().filter(  # type:ignore
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    )

    context = {
        'page_obj': posts,
        'page_title': f'Search: {search_value}',
        'search_value': search_value,
    }

    return render(
        request,
        'blog/pages/index.html',
        context,
    )
