from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import logout, login, authenticate
from templates.static import site_messages

from . import forms


class Login(View):
    def get(self, *args, **kwargs):
        pass


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)

        messages.success(self.request,
                         site_messages.success_logout_done)
        return redirect('recipes:index')


class Register(View):
    template_name = 'accounts/register.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'form': forms.RegisterAuthor(self.request.POST or None),
        }
        self.form = self.context['form']

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.form.is_valid():
            print(self.form.errors)
            messages.error(self.request,
                           'Algum campo de seu formulário está com erro. Verifique e tente novamente')
            return render(self.request, self.template_name, self.context)
            return redirect('accounts:register')
        # print(self.request.POST)

        return redirect('accounts:register')


class Login(View):
    template_name = 'accounts/login.html'

    def get(self, *args, **kwargs):

        self.context = {
            'form': forms.LoginAuthor(self.request.POST or None),
        }

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        user = authenticate(self.request,
                            email=email,
                            password=password)

        if user:
            login(self.requset, user)
            messages.success(self.request,
                             'Você fez login com sucesso')
            return redirect('recipes:index')

        messages.error(self.request,
                       'E-mail ou senha incorretos')
        return redirect('accounts:login')
