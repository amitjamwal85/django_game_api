from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from DjangoDRF import settings
from DjangoDRF.exceptions import MissingAPIVersion
from rest_framework.response import Response


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

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        if not settings.TESTING:
            u = get_user_jwt(request)
            try:
                request.user = User.objects.get(id=u.id)
            except Exception:
                # raise Response( {"status": "failed"}, status=status.HTTP_401_UNAUTHORIZED )
                raise MissingAPIVersion({"status": "fix auth token"})

        # TODO re-enable
        # api_version = get_api_version(request)
        # try:
        #     UserAppVersion.objects.create(user=request.user, app_version=api_version)
        # except Exception:
        #     # we gracefully don't give a crap :)
        #     pass

        # if not isinstance(request.user, (AnonymousUser,)):
        #     cip = get_client_ip(request)
        #     ip_info = ipapi_request(cip)
        #
        #     uipt = UserIPTrack.objects.create(user=request.user, ip=cip)
        #
        #     ul = UserLocation.objects.create(
        #         user=request.user,
        #         ip=uipt,
        #         country=ip_info.get("country_name"),
        #         region=ip_info.get("region_name"),
        #         city=ip_info.get("city"),
        #     )
        #
        #     ucl, _ = UserCurrentLocation.objects.get_or_create(user=request.user)
        #     ucl.user_location = ul
        #     ucl.save()

        return request.user and request.user.is_authenticated
