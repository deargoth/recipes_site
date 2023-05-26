from django.contrib import admin

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "author",
        "created_at",
        "updated_at",
        "is_published",
    )

    list_display_links = ("id", "title")
    list_editable = ("is_published",)
    list_select_related = ("author",)
    # autocomplete_fields = ('tags', ),
    prepopulated_fields = {
        "slug": ("title",),
    }


admin.site.register(models.Category)
