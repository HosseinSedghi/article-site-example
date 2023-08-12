from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from django.http import JsonResponse

from account_module.forms import RegisterForm, LoginForm, ForgetPasswordForm, ChangePasswordForm
from account_module.models import User


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'account_module/register.html', {
            'register_form': register_form
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            confirm_password = register_form.cleaned_data.get('confirm_password')

            is_username_exist = User.objects.filter(username__exact=username).first()
            if not is_username_exist:
                is_email_exist = User.objects.filter(email__exact=email).first()
                if not is_email_exist:
                    if password == confirm_password:
                        new_user = User(username=username, email=email, is_active=False,
                                        email_active_code=get_random_string(72))
                        new_user.set_password(password)
                        new_user.save()
                        # todo: send email for activate account
                    else:
                        register_form.add_error('confirm_password', 'password is not confirm')
                else:
                    register_form.add_error('email', 'this email used before')
            else:
                register_form.add_error('username', 'username used before')
        return render(request, 'account_module/register.html', {
            'register_form': register_form
        })


class EmailActivateView(View):
    def get(self, request, code):
        user = User.objects.filter(email_active_code__contains=code).first()

        if not user.is_active:
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            return redirect('login-page')


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'account_module/login.html', {
            'login_form': login_form
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = User.objects.filter(username__exact=username).first()
            if user:
                if user.is_active:
                    if user.check_password(password):
                        login(request, user)
                        return redirect('home-page')
                    else:
                        login_form.add_error('password', 'نام کاربری یا کلمه عبور صحیح نمی باشد')
                else:
                    login_form.add_error('username', 'حساب کاربری شما فعال نمی باشد')
            else:
                login_form.add_error('username', 'نام کاربری یا کلمه عبور صحیح نمی باشد')
        return render(request, 'account_module/login.html', {
            'login_form': login_form
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home-page')


class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, 'account_module/forget-password.html', {
            'forget_form': form
        })

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            user = User.objects.filter(email__exact=email)
            if user:
                # todo: send email for reset password
                pass
            else:
                form.add_error('email', 'email is not exist')
        return render(request, 'account_module/forget-password.html', {
            'forget_form': form
        })


class ChangePasswordView(View):
    def get(self, request, code):
        form = ChangePasswordForm()
        return render(request, 'account_module/change-password.html', {
            'change_password_form': form,
            'code': code
        })

    def post(self, request, code):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = User.objects.filter(email_active_code__exact=code).first()
            if password == confirm_password:
                user.set_password(password)
                user.email_active_code = get_random_string(72)
                user.save()
            else:
                form.add_error('confirm_password', 'password not again')
        return render(request, 'account_module/change-password.html', {
            'change_password_form': form,
            'code': code
        })