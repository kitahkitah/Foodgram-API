"""Сериализаторы для модели и эндпоинтов пользователей."""

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        """Валидировать поле username.

        Значение не должно быть равно 'me'.
        """
        if value == 'me':
            raise serializers.ValidationError({'username': 'Имя "me" запрещено!'})
        return value
