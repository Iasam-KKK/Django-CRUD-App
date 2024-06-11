# utils.py
import json
from datetime import datetime
from requests import Session
from .models import Token
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

def get_user_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token.payload.get('user_id')
    return user_id

def fetch_token_data(symbol=None):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '61d3d338-4fa3-4ffc-8c6e-0caef568bb9b',
    }

    session = Session()
    session.headers.update(headers)

    try:
        print(f"[{timezone.now()}] Cron job fetching data from API for symbol: {symbol if symbol else 'all'}")
        response = session.get(url, params=parameters)
        print(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"API Error: {response.content}")
            return None
        data = json.loads(response.text)
        tokens_data = data['data']
        print(f"Fetched {len(tokens_data)} tokens")
    
        if symbol:
            token_data = next((item for item in tokens_data if item['symbol'] == symbol.upper()), None)
            if token_data:
                print(f"Found data for {symbol}: {token_data['name']}")
                update_token_in_db(token_data)
                return token_data
            else:
                print(f"Token {symbol} not found in API response.")
                return None
        else:
            for token in tokens_data:
                update_token_in_db(token)
            return tokens_data
    except Exception as e:
        print(f"Error in fetch_token_data: {e}")
        return None

def update_token_in_db(token_data):
    token_id = token_data['id']
    symbol = token_data['symbol']
    name = token_data['name']
    price = token_data['quote']['USD']['price']
    volume_24h = token_data['quote']['USD']['volume_24h']
    volume_change_24h = token_data['quote']['USD']['volume_change_24h']
    percent_change_1h = token_data['quote']['USD']['percent_change_1h']
    percent_change_24h = token_data['quote']['USD']['percent_change_24h']
    percent_change_7d = token_data['quote']['USD']['percent_change_7d']
    market_cap = token_data['quote']['USD']['market_cap']
    market_cap_dominance = token_data.get('market_cap_dominance', 0)
    fully_diluted_market_cap = token_data.get('fully_diluted_market_cap', 0)
    last_updated = datetime.strptime(token_data['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ')

    Token.objects.update_or_create(
        token_id=token_id,
        defaults={
            'name': name,
            'symbol': symbol,
            'price': price,
            'volume_24h': volume_24h,
            'volume_change_24h': volume_change_24h,
            'percent_change_1h': percent_change_1h,
            'percent_change_24h': percent_change_24h,
            'percent_change_7d': percent_change_7d,
            'market_cap': market_cap,
            'market_cap_dominance': market_cap_dominance,
            'fully_diluted_market_cap': fully_diluted_market_cap,
            'last_updated': last_updated,
        }
    )