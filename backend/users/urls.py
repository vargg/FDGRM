from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ModifiedDjoserUserViewSet, SubscriptionsView

router = DefaultRouter()
router.register('', ModifiedDjoserUserViewSet)

urlpatterns = [
    path(
        'subscriptions/',
        SubscriptionsView.as_view(),
        name='subscriptions_view',
    ),
    path('', include(router.urls)),
]
