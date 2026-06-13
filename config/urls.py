from django.contrib import admin
from django.urls import path, include

from routes.views import home

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [

    # Home Page
    path(
        '',
        home
    ),

    # Django Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # API Routes
    path(
        'api/',
        include('routes.urls')
    ),

    # OpenAPI Schema
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]