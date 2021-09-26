from django.contrib.auth import get_user_model

from .serializers import ModifiedDjoserUserSerializer

from recipes.models import Recipe  # isort: skip
from recipes.serializers import RecipeSerializer  # isort: skip

User = get_user_model()


def subscribe_context(request, author, recipes_limit):
    author_srlz = ModifiedDjoserUserSerializer(
        author,
        context={'request': request},
    )
    all_recipes_by_author = Recipe.objects.filter(
        author=author
    )

    try:
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            all_recipes_by_author = all_recipes_by_author[:recipes_limit]
    except ValueError:
        pass

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
