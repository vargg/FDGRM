from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='Ссылка',
    )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(name={self.name}, '
            f'color={self.color}, slug={self.slug})'
        )

    def __str__(self):
        return f'{self.__class__.__name__} "{self.name}"'

    class Meta:
        ordering = ('name', )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единицы измерения',
    )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(name={self.name}, measurement_unit={self.measurement_unit})'
        )

    def __str__(self):
        return f'{self.__class__.__name__} "{self.name}"'

    class Meta:
        ordering = ('name', )


class IngredientInRecipe (models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='all_ingredients',
    )
    amount = models.IntegerField()

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ingredient',
                    'recipe',
                ],
                name='unique_ingredient_in_recipe',
            ),
        ]


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Придумайте название для рецепта'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Здесь опишите последовательность действий',
    )
    image = models.ImageField(
        upload_to='images/%Y/%m/%d',
        verbose_name='Изображение',
        help_text='Приложите подходящее фото'
    )
    # > 1 минуты
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время, необходимое для приготовления'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        help_text='Укажите список требуемых ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        help_text='Нужно указать хотя бы один тэг'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ('-created', )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(name={self.name}, '
            f'text={self.text}, image={self.image}, '
            f'cooking_time={self.cooking_time}, author={self.author}, '
            f'ingredients={self.ingredients}, tags={self.tags}, '
            f'created={self.created}'
        )

    def __str__(self):
        return f'{self.__class__.__name__} "{self.name}"'