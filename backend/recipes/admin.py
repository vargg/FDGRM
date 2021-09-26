from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingList, Tag)


class IngredientInLine(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'cooking_time',
        'in_favorites',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
        'author',
        'tags',
    )
    inlines = [
        IngredientInLine,
    ]

    def in_favorites(self, obj):
        return obj.recipe_in_favorite.count()

    in_favorites.short_description = 'В избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_display_links = (
        'user',
    )
    search_fields = (
        'user',
        'recipe',
    )


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_display_links = (
        'user',
    )
    search_fields = (
        'user',
        'recipe',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)

admin.site.site_title = admin.site.site_header = 'Админка'
