from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.http import Http404

from templates.static import site_messages
from accounts import forms
from recipes.models import Recipe


class EditRecipe(View):
    template_name = 'accounts/edit_recipe.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.pk = self.kwargs.get('pk')

        try:
            self.recipe = Recipe.objects.get(pk=self.pk)
        except:
            raise Http404()

        self.context = {
            'form': forms.EditRecipeForm(data=request.POST or None,
                                         files=request.FILES or None,
                                         instance=self.recipe,),
            'recipe': self.recipe,
        }
        self.form = self.context['form']

        self.render = render(request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            messages.error(self.request,
                           site_messages.error['login_required'])
            return redirect('accounts:login')

        if self.recipe.author != user and not user.is_superuser:
            messages.error(self.request,
                           site_messages.error['permission_required'])
            return redirect('recipes:index')

        return self.render

    def post(self, *args, **kwargs):
        if not self.form.is_valid():
            return self.render

        self.form.save(commit=False)

        self.form.author = self.request.user
        self.form.is_published = False
        self.form.preparation_steps_is_html = False

        self.form.save()

        messages.success(self.request,
                         site_messages.success['recipe_updated'])
        return redirect('accounts:edit_recipe', self.pk)
