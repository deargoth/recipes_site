from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Recipe
from ..serializers import RecipeSerializer


class RecipeAPIv2List(APIView):
    recipes = Recipe.objects.filter(is_published=True)

    def get(self, *args, **kwargs):
        serializer = RecipeSerializer(instance=self.recipes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        serializer = RecipeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeAPIv2Details(APIView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get("pk", None)
        self.recipe = Recipe.objects.filter(pk=pk).first()

    def get(self, *args, **kwargs):
        serializer = RecipeSerializer(instance=self.recipe, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        serializer = RecipeSerializer(
            instance=self.recipe, data=self.request.data, many=False, partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
