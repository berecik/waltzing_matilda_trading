"""
URL configuration for waltzing_matilda_trading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from api.views import api
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]

drf_patterns = []


if settings.DJANGO_ALLAUTH:
    urlpatterns.append(path('accounts/', include('allauth.urls')))

if settings.DRF:
    from rest_framework.authtoken import views as auth_token_views

    urlpatterns += drf_patterns
    urlpatterns.append(path('api-token-auth/', auth_token_views.obtain_auth_token, name='api-token-auth'), )
    # urlpatterns.append(
    #     path(
    #         "redoc/",
    #         TemplateView.as_view(
    #             template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
    #         ),
    #         name="redoc",
    #     ),
    # )

if settings.DJANGO_CMS:
    urlpatterns.append(path('', include('cms.urls')))

if settings.TAGGIT:
    urlpatterns.append(path('taggit_autosuggest/', include('taggit_autosuggest.urls')))

if settings.DOCS:

    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))
                   ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
                          )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.
                          STATIC_ROOT)

