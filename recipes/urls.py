from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from .views import RecipeAPIv2Viewset

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
    path("recipes/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "recipes/api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("recipes/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]


urlpatterns = views_urls + api_urls
