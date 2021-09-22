# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer

User = get_user_model()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
