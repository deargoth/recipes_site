from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('recipes/theory/', views.theory, name="theory"),
    path('recipes/api/v1/', views.IndexApi.as_view(), name="index_api"),
    path('recipes/<str:category_name>',
         views.CategoriesPage.as_view(), name="category"),
    path('recipes/details/<int:pk>', views.Details.as_view(), name="details"),
    path('recipes/details/api/v1/<int:pk>',
         views.DetailsApi.as_view(), name="details_api"),
    path('recipes/search/', views.Search.as_view(), name="search"),
]
