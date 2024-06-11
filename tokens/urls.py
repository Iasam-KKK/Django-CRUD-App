# urls.py
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AddTokenView, TokenView, CryptoInfoView

schema_view = get_schema_view(
    openapi.Info(
        title="Cryptocurrency API",
        default_version='v1',
        description="API for managing cryptocurrency tokens",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/addtoken/', AddTokenView.as_view(), name='add-token'),
    path('api/tokens/', TokenView.as_view(), name='token-list'),
    path('api/tokens/<str:symbol>/', TokenView.as_view(), name='token-detail'),
    path('api/cryptoinfo/', CryptoInfoView.as_view(), name='crypto-info'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]