# views.py
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Token, UserToken
from rest_framework import status
from .serializers import AddTokenSerializer, TokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import get_user_from_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

class AddTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
    )

    def post(self, request, *args, **kwargs):
        user_id = get_user_from_token(request)
        user = User.objects.get(id=user_id)
        serializer = AddTokenSerializer(data=request.data)
        if serializer.is_valid():
            token, quantity = serializer.save()
            user_token, created = UserToken.objects.get_or_create(user=user, token=token, defaults={'quantity': quantity})
            if not created:
                user_token.quantity += quantity
                user_token.save()
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = get_user_from_token(request)
        user = User.objects.get(id=user_id)
        tokens = Token.objects.filter(users=user)
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)