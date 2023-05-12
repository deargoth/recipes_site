from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline


from . import models
from tag.models import Tag


class TagInline(GenericStackedInline):
    model = Tag
    fields = ('name',)
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author',
                    'created_at', 'updated_at', 'is_published')

    list_display_links = ('id', 'title')
    list_editable = ('is_published', )
    inlines = [
        TagInline,
    ]


admin.site.register(models.Category)
admin.site.register(models.Recipe, RecipeAdmin)
