from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from account_module.models import User
from article_module.forms import ArticleCommentForm
from article_module.models import Article, ArticleComments, ArticleView
from packages.get_user_ip import get_user_ip


# Create your decorators here.

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


# Create your views here.


class HomeView(TemplateView):
    template_name = 'article_module/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ArticleListView(View):
    def get(self, request):
        articles = Article.objects.select_related('author').filter(status='publish')
        search_text = request.GET.get('search')
        page_number = request.GET.get('page')

        if search_text:
            articles = Article.objects.select_related('author').filter(status='publish', title__icontains=search_text)
        else:
            search_text = ''

        paginator = Paginator(articles, 4)
        page_obj = paginator.get_page(page_number)

        return render(request, 'article_module/article-list.html', {
            'page_obj': page_obj,
            'search_text': search_text
        })


class SpecialArticleListView(View):
    def get(self, request):
        articles = Article.objects.select_related('author').filter(status='publish', is_special=True)
        search_text = request.GET.get('search')
        page_number = request.GET.get('page')

        if search_text:
            articles = Article.objects.select_related('author').filter(status='publish', is_special=True,
                                                                       title__icontains=search_text)
        else:
            search_text = ''

        paginator = Paginator(articles, 4)
        page_obj = paginator.get_page(page_number)

        return render(request, 'article_module/article-list.html', {
            'page_obj': page_obj,
            'search_text': search_text
        })


class AuthorArticleListView(View):
    def get(self, request, id):
        articles = Article.objects.select_related('author').filter(status='publish', author_id=id)
        search_text = request.GET.get('search')
        page_number = request.GET.get('page')
        author = User.objects.get(id=id)

        if search_text:
            articles = Article.objects.select_related('author').filter(status='publish', author_id=id,
                                                                       title__icontains=search_text)
        else:
            search_text = ''

        paginator = Paginator(articles, 4)
        page_obj = paginator.get_page(page_number)

        return render(request, 'article_module/article-list.html', {
            'page_obj': page_obj,
            'search_text': search_text,
            'author_id': id,
            'users': author
        })

@method_decorator(special_required, name='dispatch')
class ArticleDetailView(View):
    def get(self, request, slug):
        article = Article.objects.prefetch_related('category').select_related('author').get(slug=slug, status='publish')
        comment_form = ArticleCommentForm()
        comments = ArticleComments.objects.select_related('replay').filter(is_publish=True, article=article,
                                                                           replay=None)
        comments_count = ArticleComments.objects.filter(is_publish=True, article=article).count()
        ip = get_user_ip(request)
        view = ArticleView.objects.filter(ip=ip, article=article).first()
        if not view:
            if request.user.is_authenticated:
                new_view = ArticleView(ip=ip, article_id=article.id, user_id=request.user.id)
            else:
                new_view = ArticleView(ip=ip, article_id=article.id)
            new_view.save()

        views = ArticleView.objects.select_related('article').filter(article_id=article.id).count()
        return render(request, 'article_module/article-detail.html', {
            'article': article,
            'comment_form': comment_form,
            'comments': comments,
            'comments_count': comments_count,
            'views': views
        })

    def post(self, request, slug):
        comment_form = ArticleCommentForm(request.POST)
        article = Article.objects.get(slug=slug)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data.get('comment')
            replay = comment_form.cleaned_data.get('replay')

            new_comment = ArticleComments(author_id=request.user.id, text=comment_text,
                                          article_id=article.id, replay_id=replay)
            new_comment.save()

        return redirect('article-detail-page', slug=slug)
