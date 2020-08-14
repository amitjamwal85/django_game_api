from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework.views import exception_handler
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken as InvalidTokenJWT
from rest_framework import status
from rest_framework.exceptions import APIException


class MissingAPIVersion(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'error': True,
        'data': [{'token': 'JWT token is missing'}]
        }
    default_code = 'not_authenticated'


def get_user_jwt(request):
    user = get_user(request)
    if not isinstance(user, AnonymousUser):
        if user.is_authenticated:
            return user
    try:
        user_jwt = JWTAuthentication().authenticate(request)
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        if not False:
            u = get_user_jwt(request)
            try:
                request.user = User.objects.get(id=u.id)
            except Exception:
                raise MissingAPIVersion()
        return request.user and request.user.is_authenticated


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, InvalidTokenJWT):
        custom_response_data = {
            'error': True,
            'data': [{'token': 'Invalid token'}]
        }
        response.data = custom_response_data
    return response
