from rest_framework.exceptions import APIException

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            if not isinstance(value, list):
                value = [value]
            for v in value:
                errors.append(v.replace("This field", "{} field".format(field)))

        response.data['errors'] = errors
        response.data['status'] = False

    return response


class MissingAPIVersion(APIException):

    pass


class ClassificationAddError(APIException):
    pass


class ClassificationRemoveError(APIException):
    pass


class ClassificationUserGetError(APIException):
    pass


class UserStateError(APIException):
    pass


class EmailVerificationFailed(APIException):
    pass


class DeleteSongTrackError(APIException):
    pass


class DeleteSongError(APIException):
    pass


class GetSongError(APIException):
    pass


class LyricError(APIException):
    pass


class UserError(APIException):
    pass


class PlaylistError(APIException):
    pass


class PlaylistSongError(APIException):
    pass


class SongTrackError(APIException):
    pass


class TokenError(APIException):
    pass


class InvalidToken(APIException):
    pass


class NotificationError(APIException):
    pass
