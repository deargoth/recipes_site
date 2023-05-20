from rest_framework.routers import SimpleRouter
from .views import RecipeAPIv2Viewset
from django.urls import path, include
from . import views

app_name = "recipes"

recipes_api_v2_router = SimpleRouter()
recipes_api_v2_router.register("recipes/api/v2", RecipeAPIv2Viewset, "recipes-api")

views_urls = [
    path("", views.Index.as_view(), name="index"),
    path(
        "recipes/<str:category_name>", views.CategoriesPage.as_view(), name="category"
    ),
    path("recipes/details/<int:pk>", views.Details.as_view(), name="details"),
    path("recipes/search/", views.Search.as_view(), name="search"),
    path("recipes/tags/<slug>", views.Tags.as_view(), name="tags"),
]

api_urls = [
    # V1 - Hard coded version - Understanding
    path("recipes/api/v1/", views.IndexApi.as_view(), name="index_api"),
    path(
        "recipes/details/api/v1/<int:pk>",
        views.DetailsApi.as_view(),
        name="details_api",
    ),
    # V2 - Using Django Rest
    path("", include(recipes_api_v2_router.urls)),
]


urlpatterns = views_urls + api_urls
