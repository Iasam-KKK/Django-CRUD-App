# updater.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .utils import fetch_token_data
from .models import UserToken

def update_token_data():
    try:
        print(f"\n[{timezone.now()}] Cron job running: update_token_data")
        user_tokens = UserToken.objects.values_list('token__token_id', flat=True).distinct()
        if user_tokens:
            tokens_data = fetch_token_data(user_tokens)
            if tokens_data:
                print(f"Fetched and updated {len(tokens_data)} tokens in the database.")
            else:
                print("Failed to fetch token data.")
        else:
            print("No user-added tokens to update.")

        # Update user last_online
        updated = UserToken.objects.update(last_online=timezone.now())
        print(f"Updated {updated} user(s) last_online")
    except Exception as e:
        print(f"Error in update_token_data: {e}")

def start_updater():
    print("Token updater cron job registered.")
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_token_data, 'interval', seconds=45)
    scheduler.start()