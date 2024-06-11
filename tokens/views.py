# views.py
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Token, UserToken
from .utils import fetch_token_data
from rest_framework import status
from .serializers import AddTokenSerializer, TokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import get_user_from_token

User = get_user_model()

class AddTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = get_user_from_token(request)
        user = User.objects.get(id=user_id)
        serializer = AddTokenSerializer(data=request.data)
        if serializer.is_valid():
            token, quantity = serializer.save()
            UserToken.objects.update_or_create(
                user=user,
                token=token,
                defaults={'quantity': quantity}
            )
            return Response({"message": "Token added successfully", "token": token.symbol}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(APIView):
    def get(self, request, symbol=None):
        if symbol:
            tokens = Token.objects.filter(symbol__iexact=symbol)
        else:
            tokens = Token.objects.all()
            serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data)

class CryptoInfoView(APIView):
    def get(self, request, *args, **kwargs):
        tokens_data = fetch_token_data()
        if tokens_data:
            return Response(tokens_data, status=status.HTTP_200_OK)
        return Response({"error": "Failed to fetch token data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)