from django.contrib.auth import get_user_model

from recipes.models import Recipe  # isort: skip
from recipes.serializers import RecipeSerializer  # isort: skip
from .serializers import ModifiedDjoserUserSerializer  # isort: skip

User = get_user_model()


def subscribe_context(request, author, recipes_limit):
    author_srlz = ModifiedDjoserUserSerializer(
        author,
        context={'request': request},
    )
    all_recipes_by_author = Recipe.objects.filter(
        author=author
    )

    if recipes_limit is not None and recipes_limit.isdigit():
        all_recipes_by_author = all_recipes_by_author[:int(recipes_limit)]

    recipes_count = all_recipes_by_author.count()
    recipes_srlz = RecipeSerializer(
        all_recipes_by_author,
        context={'request': request},
        many=True,
    )
    context = author_srlz.data
    context['recipes'] = recipes_srlz.data
    context['recipes_count'] = recipes_count
    return context
