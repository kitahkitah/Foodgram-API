from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('/', include(router.urls)),
]