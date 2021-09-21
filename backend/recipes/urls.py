from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientView, RecipeViewSet, TagView

# DownloadShoppingCart, FavoriteView, ShoppingCart

router = DefaultRouter()
router.register(
    'ingredients',
    IngredientView,
    basename='ingredients',
)
router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)
router.register(
    'tags',
    TagView,
    basename='tags',
)

urlpatterns = [
    # path(
    #     '/recipes/<int:id>/favorite/',
    #     FavoriteView.as_view(),
    #     name='favorite',
    # )
    # path(
    #     'recipes/<int:id>/shopping_cart/',
    #     ShoppingCart.as_view(),
    #     name='shopping_cart',
    # )
    # path(
    #     'recipes/download_shopping_cart/',
    #     DownloadShoppingCart.as_view(),
    #     name='download_shopping_cart',
    # )
    path('', include(router.urls))
]


# OK http://localhost/api/ingredients/ список ингредиентов
# OK http://localhost/api/ingredients/{id}/ ингредиент
# OK http://localhost/api/recipes/{id}/favorite/ добавить/удалить рецепт в избранное
# OK http://localhost/api/recipes/ рецепты и создание рецепта
# OK http://localhost/api/recipes/{id}/ получение, обновление и удаление рецепта
# http://localhost/api/recipes/{id}/shopping_cart/ добавить/удалить рецепт в список покупок
# http://localhost/api/recipes/download_shopping_cart/ скачать список покупок
# OK http://localhost/api/tags/ теги
# OK http://localhost/api/tags/{id}/ тэг
