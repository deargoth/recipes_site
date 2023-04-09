from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('recipes/<str:category_name>',
         views.CategoriesPage.as_view(), name="category"),
    path('details/<int:pk>', views.Details.as_view(), name="details"),
    path('recipes/search/', views.Search.as_view(), name="search"),
]
