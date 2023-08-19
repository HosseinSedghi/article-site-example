from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from account_module.models import User
from admin_panel.forms import ArticleCreateEditForm, CategoryCreateEditForm, ChangePasswordForm
from article_module.models import Article, ArticleCategory, ArticleComments
from contact_module.models import Ticket
from site_module.models import SiteSetting, Slider


# Create your views here.

# ==================================== Decorators ==================================== #

def special_required(func):
    def wrapper(request: HttpResponse, slug, *args, **kwargs):
        article = Article.objects.get(slug=slug)
        if article.is_special:
            if request.user.is_authenticated:
                if article.author.id == request.user.id:
                    return func(request, slug, *args, **kwargs)
                else:
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
        article_add_slider = request.GET.get('article_add_slider')
        article_delete_slider = request.GET.get('article_delete_slider')

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

        if article_add_slider:
            article = Article.objects.filter(id=article_add_slider).first()
            new_slider = Slider(article_id=article.id)
            new_slider.save()
            return render(request, 'admin_panel/article/article-box.html', {
                'page_obj': page_obj,
                'authors': authors,
                'author_filter': author_filter,
                'status_filter': status_filter,
                'search_text': search_text,
                'article_count': Article.objects.all().count()
            })
        if article_delete_slider:
            Slider.objects.filter(article_id=article_delete_slider).first().delete()
            return render(request, 'admin_panel/article/article-box.html', {
                'page_obj': page_obj,
                'authors': authors,
                'author_filter': author_filter,
                'status_filter': status_filter,
                'search_text': search_text,
                'article_count': Article.objects.all().count()
            })
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
        categories = ArticleCategory.objects.all()
        authors = User.objects.filter(Q(is_author=True) | Q(is_superuser=True))
        return render(request, 'admin_panel/article/article-create-edit.html', {
            'categories': categories,
            'authors': authors,
        })

    def post(self, request):
        print('creating')
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        image = request.POST.get('image')
        category = request.POST.get('category')
        is_special = request.POST.get('is_special')
        status = request.POST.get('status')
        author = request.POST.get('author')
        text = request.POST.get('text')

        print(category)
        print(type(category))
        article_exists = Article.objects.filter(Q(title__exact=title) | Q(slug__exact=slug)).exists()
        if not article_exists:
            new_article = Article(title=title, slug=slug, image=image, text=text, author_id=author)
            if is_special:
                new_article.is_special = True
            else:
                new_article.is_special = False
            if request.user.superuser:
                new_article.status = status
            else:
                if status not in ['draft', 'lock']:
                    new_article.status = 'draft'
            new_article.save()

        return render(request, 'admin_panel/article/article-create-edit.html', {})


# ==================================== Category Classes ==================================== #

class AdminCategoryListView(ListView):
    model = ArticleCategory
    template_name = 'admin_panel/category/category-list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        query = super().get_queryset()
        return query.prefetch_related('parent').filter(parent=None)


@method_decorator(view_just_admin, name='dispatch')
class AdminCategoryCreateView(CreateView):
    model = ArticleCategory
    form_class = CategoryCreateEditForm
    template_name = 'admin_panel/category/category-create-edit.html'
    success_url = reverse_lazy('admin-category-list-page')


@method_decorator(view_just_admin, name='dispatch')
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
            comments = ArticleComments.objects.select_related('author').select_related('article').filter(replay=None)
        else:
            comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                article__author_id=request.user.id, replay=None)
        article_filter = request.GET.get('article_filter')
        status_filter = request.GET.get('status_filter')

        if request.user.is_superuser:
            if article_filter and status_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=True, replay=None)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=False, replay=None)
            elif article_filter and not status_filter:
                comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                    article__title=article_filter, replay=None)
            elif status_filter and not article_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=True, replay=None)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=False, replay=None)
        else:
            if article_filter and status_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=True, article__author_id=request.user.id, replay=None)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        article__title=article_filter, is_publish=False, article__author_id=request.user.id, replay=None)
            elif article_filter and not status_filter:
                comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                    article__title=article_filter, article__author_id=request.user.id, replay=None)
            elif status_filter and not article_filter:
                if status_filter == 'publish':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=True, article__author_id=request.user.id, replay=None)
                elif status_filter == 'draft':
                    comments = ArticleComments.objects.select_related('author').select_related('article').filter(
                        is_publish=False, article__author_id=request.user.id, replay=None)

        if not status_filter:
            status_filter = ''
        if not article_filter:
            article_filter = ''
        paginator = Paginator(comments, 6)
        page_obj = paginator.get_page(request.GET.get('page'))

        no_comment_view = ArticleComments.objects.filter(is_view_by_admin=False, article__author_id=request.user.id)
        for i in no_comment_view:
            i.is_view_by_admin = True
            i.save()

        return render(request, 'admin_panel/comments.html', {
            'page_obj': page_obj,
            'article_filter': article_filter,
            'status_filter': status_filter,
            'comment_count': ArticleComments.objects.all().count(),
            'articles': Article.objects.all(),
        })

    def post(self, request):
        comment_text = request.POST.get('comment_replay')
        comment_id = request.POST.get('comment_id')
        article_id = request.POST.get('article_id')

        new_comment = ArticleComments(article_id=article_id, text=comment_text,
                                      author_id=request.user.id, replay_id=comment_id, is_publish=True)
        new_comment.save()

        return redirect('admin-comment-page')
def delete_comment(request):
    comment_id = request.GET.get('comment_id')
    ArticleComments.objects.filter(id=comment_id).first().delete()
    return JsonResponse({
        'status': 'success'
    })


def convert_comment_publish(request):
    comment_id = request.GET.get('comment_id')
    comment = ArticleComments.objects.get(id=comment_id)
    comment.is_publish = True
    comment.save()
    if request.user.is_superuser:
        comments = ArticleComments.objects.select_related('author').select_related('article').filter(
            replay=None
        )
    else:
        comments = ArticleComments.objects.select_related('author').select_related('article').filter(
            article__author_id=request.user.id, replay=None)
    article_filter = request.GET.get('article_filter')
    status_filter = request.GET.get('status_filter')
    paginator = Paginator(comments, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/comments-box.html', {
        'page_obj': page_obj,
        'article_filter': article_filter,
        'status_filter': status_filter,
        'comment_count': ArticleComments.objects.all().count(),
        'articles': Article.objects.all()
    })


def convert_comment_draft(request):
    comment_id = request.GET.get('comment_id')
    comment = ArticleComments.objects.get(id=comment_id)
    comment.is_publish = False
    comment.save()
    if request.user.is_superuser:
        comments = ArticleComments.objects.select_related('author').select_related('article').filter(
            replay=None
        )
    else:
        comments = ArticleComments.objects.select_related('author').select_related('article').filter(
            article__author_id=request.user.id, replay=None)
    article_filter = request.GET.get('article_filter')
    status_filter = request.GET.get('status_filter')
    paginator = Paginator(comments, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/comments-box.html', {
        'page_obj': page_obj,
        'article_filter': article_filter,
        'status_filter': status_filter,
        'comment_count': ArticleComments.objects.all().count(),
        'articles': Article.objects.all()
    })


# ======================================== Ticket classes ======================================== #

@method_decorator(view_just_admin, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    template_name = 'admin_panel/tickets.html'
    context_object_name = 'tickets'
    paginate_by = 4


@view_just_admin
def delete_ticket(request):
    ticket_id = request.GET.get('ticket_id')
    Ticket.objects.filter(id=ticket_id).first().delete()
    return JsonResponse({
        'status': 'success'
    })


# ======================================== Partial classes ======================================== #

class HeaderPartial(TemplateView):
    template_name = 'includes/admin_includes/header-include.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_superuser:
            context['no_view_comment_count'] = ArticleComments.objects.filter(is_view_by_admin=False).count
            context['no_view_comments'] = ArticleComments.objects.filter(is_view_by_admin=False)[:4]
            context['no_view_ticket_count'] = Ticket.objects.filter(is_view_by_admin=False).count()
            context['no_view_tickets'] = Ticket.objects.filter(is_view_by_admin=False)[:4]
        elif self.request.user.is_author:
            context['no_view_comment_count'] = ArticleComments.objects.filter(article__author_id=self.request.user.id,
                                                                              is_view_by_admin=False).count
            context['no_view_comments'] = ArticleComments.objects.filter(article__author_id=self.request.user.id,
                                                                         is_view_by_admin=False)[:4]
        return context


class FooterPartial(TemplateView):
    template_name = 'includes/admin_includes/footer-include.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['copy_right_text'] = SiteSetting.objects.first().copy_right
        return context


class LeftSideBarPartial(TemplateView):
    template_name = 'includes/admin_includes/left-side-bar-include.html'
