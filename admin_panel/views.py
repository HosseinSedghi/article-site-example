from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from account_module.models import User
from admin_panel.forms import ArticleCreateEditForm, CategoryCreateEditForm, ChangePasswordForm
from article_module.models import Article, ArticleCategory, ArticleComments


# Create your views here.

# ==================================== Decorators ==================================== #

def special_required(func):
    def wrapper(request: HttpResponse, slug, *args, **kwargs):
        article = Article.objects.get(slug=slug)
        if article.is_special:
            if request.user.is_authenticated:
                if not request.user.is_special_user:
                    return redirect(reverse_lazy('article-list-page'))
                else:
                    return func(request, slug, *args, **kwargs)
            else:
                return redirect(reverse_lazy('article-list-page'))
        else:
            return func(request, slug, *args, **kwargs)

    return wrapper


def view_just_admin(func):
    def wrapper(request: HttpResponse, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return redirect('admin-home-page')

    return wrapper


def view_the_user_or_admin(func):
    def wrapper(request: HttpResponse, pk, *args, **kwargs):
        if not request.user.is_superuser:
            if request.user.id == int(pk):
                return func(request, pk, *args, **kwargs)
            else:
                return redirect('admin-home-page')
        else:
            return func(request, pk, *args, **kwargs)

    return wrapper


def view_the_user(func):
    def wrapper(request: HttpResponse, pk, *args, **kwargs):
        if request.user.id == int(pk):
            return func(request, pk, *args, **kwargs)
        else:
            return redirect('admin-home-page')

    return wrapper


@method_decorator(login_required, name='dispatch')
class AdminHomeView(TemplateView):
    template_name = 'admin_panel/index.html'


# ==================================== Article Classes ==================================== #

class AdminArticleListView(View):
    def get(self, request):
        if request.user.is_superuser:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author_id=request.user.id)
        authors = User.objects.all()
        search_text = request.GET.get('search')
        author_filter = request.GET.get('author_filter')
        status_filter = request.GET.get('status_filter')

        if request.user.is_superuser:
            if search_text and author_filter and status_filter:
                articles = Article.objects.filter(title__icontains=search_text,
                                                  author__username__exact=author_filter,
                                                  status=status_filter)
            elif author_filter and status_filter and not search_text:
                articles = Article.objects.filter(author__username__exact=author_filter,
                                                  status=status_filter)
            elif author_filter and search_text and not status_filter:
                articles = Article.objects.filter(title__icontains=search_text,
                                                  author__username__exact=author_filter)
            elif status_filter and search_text and not author_filter:
                articles = Article.objects.filter(title__icontains=search_text,
                                                  status=status_filter)
            elif search_text and not author_filter and not status_filter:
                articles = Article.objects.filter(title__icontains=search_text)
            elif author_filter and not search_text and not status_filter:
                articles = Article.objects.filter(author__username__exact=author_filter)
            elif status_filter and not search_text and not author_filter:
                articles = Article.objects.filter(status=status_filter)
        else:
            if status_filter and search_text and not author_filter:
                articles = Article.objects.filter(title__icontains=search_text,
                                                  status=status_filter,
                                                  author_id=request.user.id)
            elif search_text and not author_filter and not status_filter:
                articles = Article.objects.filter(title__icontains=search_text,
                                                  author_id=request.user.id)
            elif status_filter and not search_text and not author_filter:
                articles = Article.objects.filter(status=status_filter,
                                                  author_id=request.user.id)

        if not search_text:
            search_text = ''
        if not status_filter:
            status_filter = ''
        if not author_filter:
            author_filter = ''
        paginator = Paginator(articles, 4)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, 'admin_panel/article/article-list.html', {
            'page_obj': page_obj,
            'authors': authors,
            'author_filter': author_filter,
            'status_filter': status_filter,
            'search_text': search_text,
            'article_count': Article.objects.all().count()
        })


class AdminArticleCreateView(View):
    def get(self, request):
        form = ArticleCreateEditForm()
        return render(request, 'admin_panel/article/article-create-edit.html', {
            'form': form
        })

    def post(self, request):
        form = ArticleCreateEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')
            is_special = form.cleaned_data.get('is_special')
            status = form.cleaned_data.get('status')
            text = form.cleaned_data.get('text')

            article_exists = Article.objects.filter(Q(title__exact=title) | Q(slug__exact=slug)).exists()
            if not article_exists:
                new_article = Article(title=title, slug=slug, image=image, category=category,
                                      is_special=is_special, text=text, author_id=request.user.id)
                if request.user.superuser:
                    new_article.status = status
                else:
                    if status not in ['draft', 'lock']:
                        new_article.status = 'draft'
                new_article.save()
            else:
                form.add_error('title', 'این نام یا اسلاگ قبلا استفاده شده است')
        return render(request, 'admin_panel/article/article-create-edit.html', {
            'form': form
        })


# ==================================== Category Classes ==================================== #

class AdminCategoryListView(ListView):
    model = ArticleCategory
    template_name = 'admin_panel/category/category-list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        query = super().get_queryset()
        return query.prefetch_related('parent').filter(parent=None)


class AdminCategoryCreateView(CreateView):
    model = ArticleCategory
    form_class = CategoryCreateEditForm
    template_name = 'admin_panel/category/category-create-edit.html'
    success_url = reverse_lazy('admin-category-list-page')


class AdminCategoryEditView(UpdateView):
    model = ArticleCategory
    form_class = CategoryCreateEditForm
    template_name = 'admin_panel/category/category-create-edit.html'
    success_url = reverse_lazy('admin-category-list-page')


# ==================================== User Classes ==================================== #

@method_decorator(view_just_admin, name='dispatch')
class AdminUserListView(View):
    def get(self, request):
        users = User.objects.all()
        search_text = request.GET.get('search')
        users_count = User.objects.all().count()

        if search_text:
            users = User.objects.filter(Q(username__icontains=search_text) | Q(first_name__icontains=search_text) | Q(
                last_name__icontains=search_text))
        else:
            search_text = ''
        paginator = Paginator(users, 4)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, 'admin_panel/users/user-list.html', {
            'page_obj': page_obj,
            'search_text': search_text,
            'users_count': users_count
        })


@method_decorator(view_the_user_or_admin, name='dispatch')
class AdminUserDetailView(DetailView):
    model = User
    template_name = 'admin_panel/users/user-detail.html'
    context_object_name = 'user'


@method_decorator(view_the_user, name='dispatch')
class AdminChangePasswordView(View):
    def get(self, request, pk):
        form = ChangePasswordForm()
        return render(request, 'admin_panel/users/user-change-password.html', {
            'form': form
        })

    def post(self, request, pk):
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = User.objects.filter(id=pk).first()
            if user:
                if user.check_password(password):
                    if new_password == confirm_password:
                        user.set_password(confirm_password)
                        user.save()
                        return render(request, 'admin_panel/users/user-change-password.html', {
                            'form': form
                        })
                    else:
                        form.add_error('confirm_password', 'پسورد تکرار شده صحیح نمی باشد')
                else:
                    form.add_error('password', 'پسورد قبلی این نیست')
            else:
                return redirect('admin-home-page')
        return render(request, 'admin_panel/users/user-change-password.html', {
            'form': form
        })


# ======================================== Comment classes ======================================== #

@method_decorator(login_required, name='dispatch')
class AdminCommentListView(View):
    def get(self, request):
        if request.user.is_superuser:
            comments = ArticleComments.objects.select_related('author').select_related('article').all()
        else:
            comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                author_id=request.user.id)
        article_filter = request.GET.get('article_filter')
        status_filter = request.GET.get('status_filter')

        if request.user.is_superuser:
            if article_filter and status_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=True)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=False)
            elif article_filter and not status_filter:
                comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                    article__title=article_filter)
            elif status_filter and not article_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=True)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=False)
        else:
            if article_filter and status_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=True, article__author_id=request.user.id)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=False, article__author_id=request.user.id)
            elif article_filter and not status_filter:
                comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                    article__title=article_filter, article__author_id=request.user.id)
            elif status_filter and not article_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=True, article__author_id=request.user.id)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=False, article__author_id=request.user.id)

        if not status_filter:
            status_filter = ''
        if not article_filter:
            article_filter = ''
        paginator = Paginator(comments, 6)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, 'admin_panel/comments.html', {
            'page_obj': page_obj,
            'article_filter': article_filter,
            'status_filter': status_filter,
            'comment_count': ArticleComments.objects.all().count(),
            'articles': Article.objects.all()
        })


# ======================================== Partial classes ======================================== #

class HeaderPartial(TemplateView):
    template_name = 'includes/admin_includes/header-include.html'


class FooterPartial(TemplateView):
    template_name = 'includes/admin_includes/footer-include.html'


class LeftSideBarPartial(TemplateView):
    template_name = 'includes/admin_includes/left-side-bar-include.html'
