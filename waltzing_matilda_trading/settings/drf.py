from .base import INSTALLED_APPS

DRF = True

# Rest Framework Token Auth
# ------------------------------------------------------------------------------
# https://dev.to/amartyadev/flutter-app-authentication-with-django-backend-1-21cp
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

INSTALLED_APPS += [
    "rest_framework",
    'rest_framework.authtoken',
    'rest_framework_gis',  # https://raphael-leger.medium.com/django-handle-latitude-and-longitude-54a4bb2f6e3b
]

DOCS = True

INSTALLED_APPS += [
    'drf_spectacular',  # docs https://drf-spectacular.readthedocs.io/en/latest/
    'drf_spectacular_sidecar',  # required for Django collectstatic discovery
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'CityExplorer API',
    'DESCRIPTION': 'Intelligent world wide tourist guide',
    'VERSION': '4.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # available SwaggerUI configuration parameters
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
}