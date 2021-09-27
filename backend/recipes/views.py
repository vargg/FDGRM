from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from config.pagination import ModifiedPageNumberPagination  # isort: skip
from .filters import RecipeFilter  # isort: skip
from .models import (  # isort: skip
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingList, Tag)
from .serializers import (  # isort: skip
    IngredientSerializer, RecipeSerializer, ShortRecipeReadOnlySerializer,
    TagSerializer)

User = get_user_model()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer
    pagination_class = ModifiedPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(
        detail=True,
        methods=['GET', 'DELETE', ],
        permission_classes=[IsAuthenticated, ],
    )
    def favorite(self, request, pk):
        return self.favorite_and_shopping_cart_performer(
            request,
            pk,
            Favorite,
        )

    @action(
        detail=True,
        methods=['GET', 'DELETE', ],
        permission_classes=[IsAuthenticated, ],
    )
    def shopping_cart(self, request, pk):
        return self.favorite_and_shopping_cart_performer(
            request,
            pk,
            ShoppingList,
        )

    def favorite_and_shopping_cart_performer(self, request, id, model):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            id=id,
        )
        if request.method == 'GET':
            _, created = model.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            if created:
                recipe_srlz = ShortRecipeReadOnlySerializer(recipe)
                return Response(
                    recipe_srlz.data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {'message': 'Рецепт уже был добавлен.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            target_recipe = model.objects.filter(
                user=user,
                recipe=recipe,
            )
            if target_recipe.exists():
                target_recipe.delete()
                return Response(
                    {'message': 'Рецепт удалён из списка.'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {'message': 'Рецепт и так не был добавлен.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class IngredientView(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = IngredientSerializer


class TagView(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = TagSerializer


class DownloadShoppingCart(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        all_ingredients = IngredientInRecipe.objects.filter(
            recipe__recipe_in_shopping_list__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        ingredients_to_buy = dict()
        for item in all_ingredients:
            name = item[0]
            if name in ingredients_to_buy:
                ingredients_to_buy[name]['amount'] += item[2]
            else:
                ingredients_to_buy[name] = {
                    'amount': item[2],
                    'measurement_unit': item[1],
                }
        pre_result = [
            f'{key}: {value["amount"]} {value["measurement_unit"]};\n'
            for key, value in ingredients_to_buy.items()
        ]
        pre_result[-1] = pre_result[-1].replace(';', '.')
        pre_result = ''.join(pre_result)
        result = 'Для выбранных рецептов понадобится:\n' + pre_result
        return HttpResponse(
            result,
            headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': 'attachment; filename="to_buy.txt"',
            }
        )
