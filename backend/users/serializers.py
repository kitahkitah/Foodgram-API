"""Сериализаторы для модели и эндпоинтов пользователей."""

from django.contrib.auth.password_validation import validate_password as valid_pass
from rest_framework import serializers

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    default_error_messages = {
        'invalid': 'Имя "me" запрещено!',
    }

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, object):
        """Проверить наличие подписки на пользователя."""
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author=object, subscriber=request.user
        ).exists()

    def validate_password(self, password):
        """Валидировать пароль встроенными валидаторами Django."""
        valid_pass(password, self.instance)
        return password

    def validate_username(self, username):
        """Валидировать username. Значение не должно быть равно 'me'."""
        if username != 'me':
            return username
        self.fail('invalid')


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя."""

    default_error_messages = {
        'incorrect_password': 'Неверный текущий пароль!',
    }

    current_password = serializers.CharField(
        max_length=150,
        required=True,
        style={'input_type': 'password'},
    )
    new_password = serializers.CharField(
        max_length=150,
        required=True,
        style={'input_type': 'password'},
    )

    def validate_current_password(self, current_password):
        """Сравнить текущий пароль с введённым."""
        if not self.context['request'].user.check_password(current_password):
            raise self.fail('incorrect_password')
        return current_password

    def validate_new_password(self, new_password):
        """Валидировать новый пароль встроенными валидаторами Django."""
        valid_pass(new_password, self.instance)
        return new_password


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена пользователя."""

    email = serializers.EmailField(write_only=True, max_length=150)
    password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )
