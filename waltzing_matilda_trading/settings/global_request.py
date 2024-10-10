from .base import MIDDLEWARE, INSTALLED_APPS

INSTALLED_APPS += ['django_middleware_global_request']
MIDDLEWARE += ['django_middleware_global_request.middleware.GlobalRequestMiddleware']
