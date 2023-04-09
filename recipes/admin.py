from django.contrib import admin
from . import models


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author',
                    'created_at', 'updated_at', 'is_published')

    list_display_links = ('id', 'title')
    list_editable = ('is_published', )


admin.site.register(models.Category)
admin.site.register(models.Recipe, RecipeAdmin)
