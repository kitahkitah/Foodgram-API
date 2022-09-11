"""Views для эндпоинтов пользователей."""

from django.contrib.auth import update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from recipes.commons import change_object_status
from .models import User
from .serializers import PasswordSerializer, TokenSerializer, UserSerializer


class UserViewSet(CreateModelMixin, ListModelMixin,
                  RetrieveModelMixin, GenericViewSet):
    """Вьюсет для эндпоинтов с пользователями."""

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.only("email", "username", "first_name", "last_name")

    def perform_create(self, serializer):
        """Присвоение зашифрованного пароля пользователю при отправке POST запроса."""
        password = serializer.validated_data.pop('password')
        instance = serializer.save()
        instance.set_password(password)
        instance.save()

    @action(['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Вернуть текущего пользователя."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(['POST'], detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=PasswordSerializer, throttle_classes=(UserRateThrottle,))
    def set_password(self, request):
        """Изменить пароль текущего пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        update_session_auth_hash(request, self.request.user)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(['POST', 'DELETE'], detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk):
        """Изменить статус подписки."""
        instance = self.get_object()
        response = change_object_status(instance, request, 'subscribed_by')
        return response

    @action(['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Получить список подписок с рецептами."""
        queryset = (request.user.subscribed_to
                    .prefetch_related('subscribed_to')
                    .prefetch_related('recipe_set'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TokenObtainView(ObtainAuthToken):
    """Представление для эндпоинта с получением токена."""

    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        """Получение токена пользователя при отправке POST запроса."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({'email': ['Неверный email!']})

        if not user.check_password(password):
            raise ValidationError({'password': ['Неверный пароль!']})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


class TokenDestroyView(APIView):
    """Представление для эндпоинта с удалением токена."""

    def post(self, request):
        """Удаление токена пользователя при отправке POST запроса."""
        Token.objects.get(user=request.user).delete()
        return Response(status=HTTP_204_NO_CONTENT)
