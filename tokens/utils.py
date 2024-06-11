# utils.py
import json
from datetime import datetime
from requests import Session
from .models import Token, UserToken
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

def get_user_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token.payload.get('user_id')
    return user_id

def fetch_token_data(token_ids=None):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '61d3d338-4fa3-4ffc-8c6e-0caef568bb9b',
    }

    session = Session()
    session.headers.update(headers)

    try:
        if token_ids:
            parameters = {
                'id': ','.join(map(str, token_ids)),
                'convert': 'USD'
            }
            print(f"[{timezone.now()}] Cron job fetching data from API for token IDs: {parameters['id']}")
            response = session.get(url, params=parameters)
            print(f"API Response Status: {response.status_code}")
            if response.status_code != 200:
                print(f"API Error: {response.content}")
                return None
            data = json.loads(response.text)
            tokens_data = data['data']
            print(f"Fetched {len(tokens_data)} tokens")
            for token in tokens_data.values():
                update_token_in_db(token)
            return tokens_data
        else:
            return None
    except Exception as e:
        print(f"Error in fetch_token_data: {e}")
        return None

def update_token_in_db(token_data):
    token_id = token_data['id']
    symbol = token_data['symbol']
    name = token_data['name']
    quote = token_data.get('quote', {})
    last_updated = datetime.strptime(token_data['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ')

    Token.objects.update_or_create(
        token_id=token_id,
        defaults={
            'name': name,
            'symbol': symbol,
            'quote': quote,
            'last_updated': last_updated,
        }
    )