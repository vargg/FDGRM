from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DownloadShoppingCart, IngredientView, RecipeViewSet, TagView

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
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
        name='download_shopping_cart',
    ),
    path('', include(router.urls)),
]
