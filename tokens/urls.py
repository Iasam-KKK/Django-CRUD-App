# urls.py
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AddTokenView, TokenView, CryptoInfoView



urlpatterns = [
    path('addtoken/', AddTokenView.as_view(), name='add-token'),
    path('tokens/', TokenView.as_view(), name='token-list'),
    path('tokens/<str:symbol>/', TokenView.as_view(), name='token-detail'),
    path('cryptoinfo/', CryptoInfoView.as_view(), name='crypto-info'),
    
]