from django.contrib.auth import get_user_model

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.serializers import AccountSerializer


User = get_user_model()


class AccountViewset(ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        qs = User.objects.filter(email=self.request.user.email)
        return qs

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def me(self, *args, **kwargs):
        obj = self.get_queryset().first()

        serializer = self.get_serializer(
            instance=obj,
        )

        return Response(data=serializer.data)
