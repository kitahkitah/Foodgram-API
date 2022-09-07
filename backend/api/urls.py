"""Эндпоинты приложения с основной логикой API."""

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import TokenDestroyView, TokenObtainView, UserViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', TokenObtainView.as_view(), name='token_obtain'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token_destroy'),
    path('', include(router.urls)),
]
