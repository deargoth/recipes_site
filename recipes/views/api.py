from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..permissions import IsOwner
from ..models import Recipe
from ..serializers import RecipeSerializer


class RecipeAPIv2Paginator(PageNumberPagination):
    page_size = 5


class RecipeAPIv2Viewset(ModelViewSet):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Paginator
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get("category_id", "")

        if category_id != "" and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsOwner(),
            ]

        return super().get_permissions()

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = self.get_queryset().filter(pk=pk).first()

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()

        serializer = RecipeSerializer(
            instance=recipe, data=request.data, many=False, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
