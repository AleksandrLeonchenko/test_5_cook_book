from django.contrib import admin
from .models import Product, Recipe, RecipeProduct


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'usage_count')
    list_display_links = ('id', 'name', 'usage_count')
    search_fields = ('id', 'name', 'usage_count')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    inlines = [RecipeProductInline]


@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'product', 'weight')
    list_display_links = ('id', 'recipe', 'product', 'weight')
    search_fields = ('recipe__name', 'product__name')


admin.site.site_title = 'Админ-панель проекта "cook"'
admin.site.site_header = 'Админ-панель проекта "cook"'