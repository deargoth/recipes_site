from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from accounts import forms
from templates.static import site_messages


class Register(View):
    template_name = "accounts/register.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.context = {
            'register_form': forms.UserRegisterForm(request.POST or None),
        }
        self.register_form = self.context['register_form']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            messages.error(self.request,
                           site_messages.error['already_logged'])
            return redirect("recipes:index")

        return self.render

    def post(self, *args, **kwargs):
        if not self.register_form.is_valid():
            return self.render

        password = self.request.POST.get('password')

        user = self.register_form.save(commit=False)
        user.set_password(password)
        user.save()

        messages.success(self.request,
                         site_messages.success['register_done'])
        return redirect("accounts:login")


class Login(View):
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.context = {
            'login_form': forms.UserLoginForm(request.POST or None),
        }
        self.login_form = self.context['login_form']

        self.render = render(request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            messages.error(self.request,
                           site_messages.error['already_logged'])
            return redirect('recipes:index')

        return self.render

    def post(self, *args, **kwargs):
        if not self.login_form.is_valid():
            return self.render

        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        is_authenticated = authenticate(self.request,
                                        email=email,
                                        password=password)

        if not is_authenticated:
            messages.error(self.request,
                           site_messages.error['wrong_credentials'])
            return redirect('accounts:login')

        login(self.request,
              is_authenticated)

        messages.success(self.request,
                         site_messages.success['successful_login'])
        return redirect('recipes:index')


@login_required(login_url='accounts:login', redirect_field_name='next')
def logout_view(request):
    logout(request)

    messages.success(request,
                     site_messages.success['logout_done'])
    return redirect('recipes:index')
