from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'material', 'stock')
    search_fields = ('name', 'material')
    filter_horizontal = ('categories',)
    fields = ('name', 'description', 'price', 'material', 'width', 'height', 'image', 'categories', 'stock')
    list_editable = ('stock',)