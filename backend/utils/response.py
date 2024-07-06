from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.serializers import ValidationError


def APIResponse(msg=None, data=None, status=None):
    response = Response()
    response.data = {
        'message': msg,
        'data': data if data else None
    }
    response.status_code = status if status else HTTP_200_OK
    return response


class CustomValidationError(ValidationError):
    def __init__(self, detail, code=None):
        if isinstance(detail, list):
            self.detail = {"message": detail[0]}
        else:
            self.detail = {"message": detail}
        self.code = code