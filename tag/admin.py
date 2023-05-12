from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'slug', )
    list_editable = ('name', )
    search_fields = ('id', 'slug', 'name')
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }

# admin.site.register(Tag, TagAdmin)
