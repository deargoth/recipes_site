from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

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
        return redirect("recipes:index")
