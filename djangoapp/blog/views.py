from django.shortcuts import redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView


PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type:ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home'
        })

        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self._temp_context['user']

        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name}'

        context.update({'page_title': f'Criado por: {user_full_name}'})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            created_by__pk=self._temp_context['user'].pk
        )

        return queryset

    def get(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_id': author_id,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = (
            f'Categoria: {self.object_list[0].category.name}'  # type:ignore
        )

        context.update(
            {'page_title': page_title}
        )

        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )


class TagListView(PostListView):
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = (
            'Tags'
        )

        context.update(
            {'page_title': page_title}
        )

        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()

        context.update({
            'page_title': f'Page: {page.title}'  # type:ignore
        })

        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context.update({
            'page_title': f'Post: {post.title}'  # type:ignore
        })

        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value

        context.update({
            'page_title': f'Search: {search_value}',
            'search_value': search_value,
        })

        return context

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
