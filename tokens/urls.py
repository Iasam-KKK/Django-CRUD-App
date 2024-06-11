# urls.py
from django.urls import path
from .views import AddTokenView, TokenView, CryptoInfoView

urlpatterns = [
    path('api/tokens/', TokenView.as_view(), name='tokens-list'),
    path('api/addtoken/', AddTokenView.as_view(), name='add-token'),
    path('api/cryptocurrency/info/', CryptoInfoView.as_view(), name='crypto-info'),
    path('api/tokens/<str:symbol>/', TokenView.as_view(), name='token-detail'),
]