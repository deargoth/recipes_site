from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ..models import Recipe
from ..serializers import RecipeSerializer


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer


class RecipeAPIv2Details(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
