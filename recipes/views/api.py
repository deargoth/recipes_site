from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import Recipe
from ..serializers import RecipeSerializer


class RecipeAPIv2Paginator(PageNumberPagination):
    page_size = 5


class RecipeAPIv2Viewset(ModelViewSet):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Paginator

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get("category_id", "")

        if category_id != "" and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        recipe = self.get_queryset().filter(pk=pk).first()

        serializer = RecipeSerializer(
            instance=recipe, data=request.data, many=False, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
