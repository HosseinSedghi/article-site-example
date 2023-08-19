from django.urls import path

from article_module import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('articles/', views.ArticleListView.as_view(), name='article-list-page'),
    path('articles-by-users/<id>', views.AuthorArticleListView.as_view(), name='users-article-list-page'),
    path('special-articles/', views.SpecialArticleListView.as_view(), name='special-article-list-page'),
    path('articles/<slug>', views.ArticleDetailView.as_view(), name='article-detail-page'),
    # Like & Dislike URLs
    # path('articles/article-like-and-unlike', views.like_and_unlike),
    # path('article-unlike', views.set_unlike),
    # path('article-dislike', views.set_dislike),
    # path('article-undislike', views.set_undislike),
]