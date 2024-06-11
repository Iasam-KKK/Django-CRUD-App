from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .utils import fetch_token_data
from .models import UserToken
from .models import Token

def update_token_data():
    try:
        print(f"\n[{timezone.now()}] Cron job running: update_token_data")
        tokens_data = fetch_token_data()
        if tokens_data:
            print(f"Fetched and updated {len(tokens_data)} tokens in the database.")
        else:
            print("Failed to fetch token data.")

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