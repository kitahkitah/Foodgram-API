"""Views для модели и эндпоинтов пользователей."""

from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import PasswordSerializer, TokenSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, GenericViewSet):
    """Вьюсет для эндпоинтов с пользователями."""

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['GET'], url_path='me',
            permission_classes=(IsAuthenticated,))
    def current_user(self, request):
        """Вернуть текущего пользователя."""
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    @method_decorator(sensitive_post_parameters())
    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        """Вернуть текущего пользователя."""
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response(status=HTTP_204_NO_CONTENT)


class TokenObtainView(ObtainAuthToken):
    """Представление для эндпоинта с получением токена."""

    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class TokenDestroyView(APIView):
    """Представление для эндпоинта с удалением токена."""

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=HTTP_204_NO_CONTENT)
