"""Views для модели и эндпоинтов пользователей."""

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет для эндпоинтов с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'], url_path='me')
    def current_user(self, request):
        """Создать эндпоинт с текущим пользователем."""
        user = self.request.user
        return Response(UserSerializer(user).data)
