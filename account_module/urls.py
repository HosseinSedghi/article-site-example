from django.urls import path

from account_module import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('activete-account/<code>', views.EmailActivateView.as_view(), name='activate-account-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('forget-password/', views.ForgetPasswordView.as_view(), name='forget-password-page'),
    path('change-password/<code>', views.ChangePasswordView.as_view(), name='change-password-page'),
]