"""Эндпоинты приложения с основной логикой API."""

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import TokenDestroyView, TokenObtainView
from users.views import UserViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', TokenObtainView.as_view(), name='token_obtain'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token_destroy'),
    path('', include(router.urls)),
]
