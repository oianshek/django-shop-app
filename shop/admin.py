from django.contrib import admin

from .models import*


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'image', 'in_stock', 'category']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    list_editable = ['in_stock', ]
    list_filter = ['in_stock', ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    search_fields = ['name',]
    prepopulated_fields = {"slug": ("name",)}