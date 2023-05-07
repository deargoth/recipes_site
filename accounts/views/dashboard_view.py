from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect

from templates.static import site_messages
from recipes.models import Recipe


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
