from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import (  # isort: skip
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingList, Tag)
from users.serializers import ModifiedDjoserUserSerializer  # isort: skip


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = [
            'name',
            'color',
            'slug',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id',
    )
    ingredient = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all(),
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientInRecipe
        fields = [
            'id',
            'ingredient',
            'measurement_unit',
            'amount',
        ]


class IngredientsSerializerField(serializers.Field):
    def to_representation(self, value):
        return IngredientInRecipeSerializer(
            IngredientInRecipe.objects.filter(recipe=value),
            many=True,
        ).data

    def to_internal_value(self, data):
        self.source_attrs = ['ingredients']
        return data


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientsSerializerField(source='*')
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = ModifiedDjoserUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def to_internal_value(self, data):
        try:
            tags_indexes = data.pop('tags')
        except KeyError:
            tags_indexes = None
        if tags_indexes is not None:
            data['tags'] = [
                {'id': i} for i in tags_indexes
            ]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields['ingredients'].source_attrs = []
        return super().to_representation(instance)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        user = request.user
        return ShoppingList.objects.filter(recipe=obj, user=user).exists()

    @transaction.atomic
    def create(self, validated_data):
        return self.performer(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        return self.performer(validated_data, instance)

    def performer(self, validated_data, recipe=None):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        if recipe is None:
            recipe = self.Meta.model.objects.create(**validated_data)
        else:
            IngredientInRecipe.objects.filter(recipe=recipe).delete()
            old_tags = Tag.objects.filter(recipe=recipe)
            for tag in old_tags:
                recipe.tags.remove(tag)
            for key, value in validated_data.items():
                setattr(recipe, key, value)
            recipe.save()
        for tag in tags:
            recipe.tags.add(tag['id'])

        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=get_object_or_404(
                        Ingredient,
                        id=ingredient['id'],
                    ),
                    amount=ingredient['amount'],
                ) for ingredient in ingredients
            ]
        )
        return recipe

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                'Нужно указать хотя бы один ингредиент.'
            )
        all_ingredients_id = list()
        for ingredient in value:
            ingredient_id = ingredient.get('id')
            ingredient_amount = ingredient.get('amount')
            if ingredient_id is None or ingredient_amount is None:
                raise serializers.ValidationError(
                    'Для ингредиентов необходимо указать номер (id) и '
                    'количество (amount).'
                )
            try:
                ingredient_id = float(ingredient_id)
                ingredient_amount = float(ingredient_amount)
            except ValueError:
                raise serializers.ValidationError(
                    'Номер (id) и количество (amount) должны быть числами.'
                )
            if ingredient_id in all_ingredients_id:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторятся.'
                )
            else:
                all_ingredients_id.append(ingredient_id)
            if ingredient_amount <= 0:
                raise serializers.ValidationError(
                    'Количество должно быть больше 0.'
                )
        return value

    def validate_cooking_time(self, value):
        try:
            cooking_time = float(value)
        except ValueError:
            raise serializers.ValidationError(
                'Время приготовления (cooking_time) должно быть числом.'
            )
        if cooking_time <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0.'
            )
        return value


class ShortRecipeReadOnlySerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
