from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.db.models import Q, Value
from django.http import Http404
from decouple import config


from .models import Recipe, Category
from templates.static import site_messages
from utils.pagination import make_pagination


PER_PAGE = int(config('PER_PAGE', 6))


class Index(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/index.html'
    paginate_by = PER_PAGE

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published=True).order_by('-id')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagination = make_pagination(context)

        context['paginator_func'] = pagination

        return context


class CategoriesPage(Index):
    template_name = 'recipes/pages/categories.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category_kwargs = self.kwargs['category_name']

        qs = qs.filter(category__name__iexact=category_kwargs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_kwargs = self.kwargs['category_name']

        context["category_name"] = category_kwargs
        return context


class Details(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_detail_page'] = True

        return context


class Details(View):
    template_name = 'recipes/pages/details.html'

    def get(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        try:
            recipe = Recipe.objects.get(pk=pk)
        except:
            messages.error(self.request,
                           site_messages.error_recipe_not_found)
            return redirect('recipes:index')

        if not recipe.is_published:
            messages.error(self.request,
                           site_messages.error_recipe_not_found)
            return redirect('recipes:index')

        self.context = {
            'recipe': recipe,
            'is_detail_page': True,
        }

        return render(self.request, self.template_name, self.context)


class Search(Index):
    model = Recipe
    template_name = 'recipes/pages/search.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        qs = super().get_queryset()

        search_term = self.request.GET.get('q', '').strip()
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        ).order_by('-id')

        if not search_term:
            raise Http404()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_term = self.request.GET.get('q', '').strip()
        context['page_title'] = f'Search for "{search_term}"'
        context['search_term'] = search_term
        context['additional_url_query'] = f'&q={search_term}'

        return context
