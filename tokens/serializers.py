from datetime import timezone
from rest_framework import serializers
from .models import Token, UserToken

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['name', 'symbol', 'price', 'volume_24h', 'volume_change_24h', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap', 'market_cap_dominance', 'fully_diluted_market_cap', 'last_updated']

class AddTokenSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=20, decimal_places=10, default=0)

    class Meta:
        model = Token
        fields = ['token_id', 'name', 'symbol', 'quantity']

    def create(self, validated_data):
        quantity = validated_data.pop('quantity', 0)
        token, created = Token.objects.update_or_create(
            token_id=validated_data['token_id'],
            defaults={
                'name': validated_data['name'],
                'symbol': validated_data['symbol'],
                'price': 0,
                'volume_24h': 0,
                'volume_change_24h': 0,
                'percent_change_1h': 0,
                'percent_change_24h': 0,
                'percent_change_7d': 0,
                'market_cap': 0,
                'market_cap_dominance': 0,
                'fully_diluted_market_cap': 0,
            }
        )
        return token, quantity

         
        