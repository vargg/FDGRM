from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Follow


class ModifiedDjoserUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(source='*')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed', )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj
        ).exists()
