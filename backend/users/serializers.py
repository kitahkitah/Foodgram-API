"""Сериализаторы для модели и эндпоинтов пользователей."""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password as pass_valid
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # переопределить!
    def get_is_subscribed(self, object):
        """Проверить наличие подписки на пользователя."""
        return False

    def validate_username(self, username):
        """
        Валидировать поле username.
        Значение не должно быть равно 'me'.
        """
        if username == 'me':
            raise serializers.ValidationError({'username': 'Имя "me" запрещено!'})
        return username

    def validate_password(self, password):
        pass_valid(password, self.instance)
        return password


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя."""

    new_password = serializers.CharField(
        max_length=150,
        required=True,
        style={'input_type': 'password'}
    )
    current_password = serializers.CharField(
        max_length=150,
        required=True,
        style={'input_type': 'password'}
    )

    def validate_current_password(self, current_password):
        """
        Валидировать действующий пароль.
        Значение должно соответствовать текущему паролю.
        """
        if not self.user.check_password(current_password):
            raise serializers.ValidationError(
                {'current_password': 'Неверный текущий пароль!'}
            )
        return current_password


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена пользователя."""

    email = serializers.EmailField(write_only=True, max_length=150)
    password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email, password = attrs.get('email'), attrs.get('password')
        # self.user = authenticate(
        #     request=self.context.get('request'),
        #     email=email, password=password
        # )
        # if not self.user:
        #     self.user = User.objects.filter(email=email).first()
        # if self.user and self.user.is_active:
        #     return attrs
        self.user = authenticate(email=email, password=password)
        if self.user and self.user.is_active:
            return attrs
        raise serializers.ValidationError(
            {'message': 'Неверные аутентификационные данные'}
        )
