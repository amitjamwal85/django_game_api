from django.conf import settings
from django.http import HttpResponse


class StackOverflowMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response( request )

    def process_exception(self, request, exception):
        if settings.DEBUG:
            print(f"middleware exception: {exception.__class__.__name__}")
            print(f"exception : {exception}")
            #return HttpResponse(f"{exception.__class__.__name__}")
        return None

