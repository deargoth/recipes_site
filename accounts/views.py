from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts import forms
from recipes.models import Recipe
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


class Dashboard(View):
    template_name = 'accounts/dashboard.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                site_messages.error['login_required']
            )
            return redirect('accounts:login')

        recipes = Recipe.objects.filter(
            author=self.request.user, is_published=False)

        count_recipes = len(recipes)

        self.context = {
            'recipes': recipes,
            'count_recipes': count_recipes,
        }

        return render(self.request, self.template_name, self.context)
