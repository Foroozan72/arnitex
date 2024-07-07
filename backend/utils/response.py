from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def APIResponse(msg=None, data=None, status=None):
    response = Response()
    response.data = {
        'messages': {'message': msg},
        'data': data if data else None
    }
    response.status_code = status if status else HTTP_200_OK
    return response

class APIResponseMixin:
    def api_response(self, msg=None, data=None, status=None):
        return APIResponse(msg=msg, data=data, status=status)
        
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            custom_response_data = {'messages': {}}
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    custom_response_data['messages'][field] = errors[0]
                else:
                    custom_response_data['messages'][field] = errors
            response.data = custom_response_data
        else:
            custom_response_data = {'messages': response.data.get('detail', 'An error occurred')}
            response.data = custom_response_data

    return response


class CustomValidationError(ValidationError):
    def __init__(self, detail, code=None):
        if isinstance(detail, (list, dict)):
            detail = detail[0] if isinstance(detail, list) else list(detail.values())[0][0]
        self.detail = {"messages": detail}
        super().__init__(self.detail, code=code)