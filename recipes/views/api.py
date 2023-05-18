from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Recipe
from ..serializers import RecipeSerializer


@api_view(http_method_names=["GET", "POST"])
def recipes_api_v2_list(request):
    recipes = Recipe.objects.filter(is_published=True)

    if request.method == "GET":
        serializer = RecipeSerializer(instance=recipes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def recipes_api_v2_details(request, pk):
    recipe = Recipe.objects.filter(pk=pk).first()

    if request.method == "GET":
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        serializer = RecipeSerializer(
            instance=recipe, data=request.data, many=False, partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
