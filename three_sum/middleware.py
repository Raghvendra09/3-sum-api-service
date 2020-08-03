from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseForbidden


def authentication_middleware(get_response):

    def middleware(request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            # return Response('Token is mandatory', status=status.HTTP_403_FORBIDDEN)
            return HttpResponseForbidden()
        if token != settings.API_ACCESS_TOKEN:
            return Response('Invalid Token', status=status.HTTP_401_UNAUTHORIZED)

        return get_response(request)
    return middleware




