# serializers.py
from datetime import datetime
from rest_framework import serializers
from .models import Token, UserToken
from .utils import fetch_token_data

class TokenSerializer(serializers.ModelSerializer):
    quote = serializers.JSONField(required=False)

    class Meta:
        model = Token
        fields = ['name', 'symbol', 'quote', 'last_updated']

class AddTokenSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=20, decimal_places=10, required=True)

    class Meta:
        model = Token
        fields = ['token_id', 'name', 'symbol', 'quantity']

    def validate_token_id(self, value):
        token_data = fetch_token_data([value])
        if not token_data:
            raise serializers.ValidationError(f"Token with ID {value} not found in the CoinMarketCap API response.")
        return value

    def create(self, validated_data):
        quantity = validated_data.pop('quantity')
        token_id = validated_data['token_id']

        token_data = fetch_token_data([token_id])
        token_data = token_data.get(str(token_id))
        token, created = Token.objects.update_or_create(
            token_id=token_id,
            defaults={
                'name': token_data['name'],
                'symbol': token_data['symbol'],
                'quote': token_data.get('quote', {}),
                'last_updated': datetime.strptime(token_data['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            }
        )
        return token, quantity