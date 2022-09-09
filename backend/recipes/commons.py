"""Общие методы для вьюсетов."""

from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


def change_object_status(instance, request, related_name):
    """Изменить статус объекта."""
    is_existent = getattr(instance, related_name).filter(id=request.user.id).exists()

    if request.method == 'POST':
        if not is_existent:
            getattr(instance, related_name).add(request.user)
            to_response = instance.__dict__
            to_response.pop('_state')
            return Response(to_response, status=HTTP_201_CREATED)
        raise ValidationError({'errors': 'Уже добавлен!'})

    if request.method == 'DELETE':
        if is_existent:
            getattr(instance, related_name).remove(request.user)
            return Response(status=HTTP_204_NO_CONTENT)
        raise ValidationError({'errors': 'Ещё не добавлен!'})
