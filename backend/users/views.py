from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import ModifiedDjoserUserSerializer
from .utils import subscribe_context

from config.pagination import ModifiedPageNumberPagination  # isort: skip

User = get_user_model()


class ModifiedDjoserUserViewSet(UserViewSet):
    pagination_class = ModifiedPageNumberPagination
    serializer_class = ModifiedDjoserUserSerializer

    @action(
        detail=True,
        methods=['GET', 'DELETE', ],
        permission_classes=[IsAuthenticated, ],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(
            User,
            pk=id,
        )
        if user != author:
            if request.method == 'GET':
                instance, created = Follow.objects.get_or_create(
                    user=user,
                    author=author,
                )
                if created:
                    recipes_limit = request.query_params.get('recipes_limit')
                    context = subscribe_context(request, author, recipes_limit)
                    return Response(
                        context,
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {'message': 'Подписка уже была оформлена.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                subscription = Follow.objects.filter(
                    user=user,
                    author=author,
                )
                if subscription.exists():
                    subscription.delete()
                    return Response(
                        {'message': 'Подписка отменена.'},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    return Response(
                        {
                            'message': (
                                'Нельзя отменить несуществующую подписку.'
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return Response(
                {'message': 'Подписаться/отписаться на самого себя нельзя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SubscriptionsView(ListAPIView):
    pagination_class = ModifiedPageNumberPagination
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = self.request.user
        list_of_authors = User.objects.filter(followers__user=user)
        page = self.paginate_queryset(list_of_authors)
        recipes_limit = request.query_params.get('recipes_limit')
        context = [
            subscribe_context(
                request,
                author,
                recipes_limit,
            ) for author in page
        ]
        return self.get_paginated_response(context)
