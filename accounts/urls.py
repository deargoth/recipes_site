from django.urls import path, include
from django.contrib.auth.views import LogoutView

from rest_framework.routers import SimpleRouter

from . import views

app_name = "accounts"

author_api_v2_router = SimpleRouter()
author_api_v2_router.register("api/v2", views.AccountViewset, "accounts-api")

print(author_api_v2_router.urls)

site_urls = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("profile/<slug>", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/<slug>", views.EditProfile.as_view(), name="edit_profile"),
    path(
        "dashboard/recipe/create/", views.CreateRecipe.as_view(), name="create_recipe"
    ),
    path(
        "dashboard/recipe/edit/<int:pk>", views.EditRecipe.as_view(), name="edit_recipe"
    ),
    path(
        "dashboard/recipe/delete/<int:pk>",
        views.DeleteRecipe.as_view(),
        name="delete_recipe",
    ),
]

api_urls = [
    path("", include(author_api_v2_router.urls)),
]

urlpatterns = site_urls + api_urls
