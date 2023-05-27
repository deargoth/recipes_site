from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from django.http import Http404

from recipes.models import Recipe
from templates.static import site_messages


class DeleteRecipe(View):
    template_name = 'accounts/dashboard.html'

    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404()

        pk = self.kwargs.get('pk')

        try:
            recipe = Recipe.objects.get(is_published=False,
                                        author=self.request.user,
                                        pk=pk,)
        except:
            messages.error(self.request,
                           site_messages.error['recipe_not_found'])
            return redirect('accounts:dashboard')

        recipe.delete()

        messages.success(self.request,
                         site_messages.success['recipe_deleted'])
        return redirect('accounts:dashboard')
