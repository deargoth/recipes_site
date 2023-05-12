from django.contrib import admin

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author',
                    'created_at', 'updated_at', 'is_published')

    list_display_links = ('id', 'title')
    list_editable = ('is_published', )
    autocomplete_fields = ('tags', )


admin.site.register(models.Category)
