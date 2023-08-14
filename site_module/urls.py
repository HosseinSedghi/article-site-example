from django.urls import path

from site_module import views

urlpatterns = [
    path('about-site', views.AboutUsView.as_view(), name='about-us-page'),
]