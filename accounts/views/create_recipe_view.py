from django.urls import render, redirect
from django.views.generic import View
from django.contrib import messages

from templates.static import site_messages
from accounts import forms


class CreateRecipe(View):
    template_name = 'accounts/create_recipe.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.context = {
            'form': forms.CreateRecipeForm(data=request.POST or None,
                                           files=request.FILES,
                                           ),
        }
        self.form = self.context['form']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           site_messages.error['login_required'])
            return redirect('accounts:login')

        return self.render

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            if not self.form.is_valid():
                return self.render

        form = self.form.save(commit=False)

        form.author = self.request.user
        form.is_published = False
        form.preparation_steps_is_html = False

        form.save()

        messages.success(self.request,
                         site_messages.success['recipe_created'])
        return redirect('recipes:index')
