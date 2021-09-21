from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientInLine(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'author',
        'cooking_time',
    )
    list_display_links = (
        'name',
        'text',
        'author',
        'cooking_time',
    )
    search_fields = (
        'name',
        'text',
        'author',
        'cooking_time',
    )
    inlines = [
        IngredientInLine,
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_display_links = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_display_links = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)

admin.site.site_title = admin.site.site_header = 'Админка'
