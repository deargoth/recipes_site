from django.utils import translation
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.http import Http404, JsonResponse
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView

from decouple import config

from .models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination


PER_PAGE = int(config('PER_PAGE', 6))


class Index(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/index.html'
    paginate_by = PER_PAGE

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published=True).order_by(
            '-id').select_related('author', 'category')

        qs = qs.prefetch_related('author__profile')

        qs = qs.annotate(author_full_name=Concat(
            F('author__first_name'),
            Value(' '),
            F('author__last_name'),
        ))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagination = make_pagination(context)
        browser_language = translation.get_language()

        context.update({
            "paginator_func": pagination,
            "html_language": browser_language,
        })

        return context


class IndexApi(Index):
    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']

        return JsonResponse(
            list(recipes.values()),
            safe=False
        )


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
    template_name = 'recipes/pages/details.html'
    context_object_name = 'recipe'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            Q(is_published=True) |
            Q(author__id=self.request.user.id)).select_related('author')

        qs = qs.annotate(author_full_name=Concat(
            F('author__first_name'),
            Value(' '),
            F('author__last_name'),
        ))

        qs = qs.prefetch_related('tags')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_detail_page': True
        })

        return context


class DetailsApi(Details):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        recipe_dict['author'] = recipe.author.get_full_name()
        recipe_dict['category'] = recipe.category.name

        if recipe_dict.get('image'):
            recipe_dict['image'] = self.request.build_absolute_uri(
            ) + recipe_dict['image'].url[1:]

        else:
            recipe_dict['image'] = ''

        del recipe_dict['is_published']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


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


class Tags(Index):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tags__slug=self.kwargs.get('slug', '')).order_by('-id')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = Tag.objects.get(slug=self.kwargs.get('slug', ''))

        if not page_title:
            page_title = _('No recipes founded | ')

        page_title = f'Tag "{page_title.name}" | '

        context.update({
            'page_title': page_title,
        })

        return context
