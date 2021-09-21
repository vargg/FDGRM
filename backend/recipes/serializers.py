from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


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
            'amount',
            'measurement_unit',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    image = Base64ImageField()
    ingredients = IngredientsSerializerField(source='*')
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def to_internal_value(self, data):
        tags_indexes = data.pop('tags')
        data['tags'] = [
            {'id': i} for i in tags_indexes
        ]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields['ingredients'].source_attrs = []
        return super().to_representation(instance)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        new_recipe = self.Meta.model.objects.create(**validated_data)

        for tag in tags:
            new_recipe.tags.add(tag['id'])

        ingredients_objects = [
            IngredientInRecipe(
                recipe=new_recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id']
                ),
                amount=ingredient['amount'],
            ) for ingredient in ingredients
        ]

        IngredientInRecipe.objects.bulk_create(ingredients_objects)
        return new_recipe
