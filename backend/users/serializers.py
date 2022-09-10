"""Сериализаторы для модели и эндпоинтов пользователей."""

from django.contrib.auth.password_validation import validate_password as valid_pass
from rest_framework import serializers

from recipes.models import Recipe
from .models import User


class PartialRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для частичной модели рецепта
    для представления внутри эндпоинта с подписками.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    default_error_messages = {
        'invalid': 'Имя "me" запрещено!',
    }

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipe_set.count', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'password', 'recipes', 'recipes_count')
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        view = self.context.get('view', False)
        if not view or view.name != 'Subscriptions':
            self.fields.pop('recipes')
            self.fields.pop('recipes_count')

    def get_is_subscribed(self, obj):
        """Проверить наличие подписки на пользователя."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.subscribed_to.filter(id=obj.id).exists()

    def get_recipes(self, obj):
        """Получить ограниченное числов рецептов на странице с подписками."""
        limit = self.context['request'].query_params.get('recipes_limit', False)
        queryset = obj.recipe_set.all()
        if limit:
            queryset = queryset[:int(limit)]
        return PartialRecipeSerializer(queryset, many=True).data

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

    email = serializers.EmailField(max_length=150, write_only=True)
    password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )
