from rest_framework import serializers


from .models import Recipe
from accounts.validators import RecipeValidatorForm


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "description",
            "slug",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "image",
            "preparation",
            "servings_concat",
            "tags",
        )

    preparation = serializers.SerializerMethodField(read_only=True)
    servings_concat = serializers.SerializerMethodField(read_only=True)

    def get_preparation(self, obj):
        return f"{obj.preparation_time} {obj.preparation_time_unit}"

    def get_servings_concat(self, obj):
        return f"{obj.servings} {obj.servings_unit}"

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        RecipeValidatorForm(data=super_validate, ErrorClass=serializers.ValidationError)

        return super_validate
