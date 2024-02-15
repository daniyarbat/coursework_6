from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Article
from blog.forms import ArticleForm


class ArticleListView(ListView):
    paginate_by = 6
    model = Article
    extra_context = {'title': 'Блог: статьи'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('-created_at')
        return queryset


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.add_article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи'
        return context


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:view_article')
    permission_required = 'blog.change_article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование статьи'
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:view_article', args=[self.kwargs.get('slug')]))


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.delete_article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление "{self.object.title}"'
        return context
