from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # زبان را از هدرهای درخواست دریافت کنید
        user_language = request.headers.get('Accept-Language', 'en')
        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language

        response = self.get_response(request)

        translation.deactivate()

        return response
