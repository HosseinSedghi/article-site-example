from django.urls import path

from article_module import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('articles/', views.ArticleListView.as_view(), name='article-list-page'),
    path('special-articles/', views.SpecialArticleListView.as_view(), name='special-article-list-page'),
    path('articles/<slug>', views.ArticleDetailView.as_view(), name='article-detail-page'),
]