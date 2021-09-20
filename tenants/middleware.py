from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TranviaMiddleware:

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)

        return response

    def process_request(self, request):
        cook_token = request.COOKIES.get('token', '')
        try:
            token = Token.objects.get(key=cook_token)
            request.user = token.user
            close_old_connections()
        except Token.DoesNotExist:
            request.user = AnonymousUser()

    def process_response(self, request, response):
        # response.COOKIES = request.COOKIES
        return response
