# models.py
from django.db import models
from django.conf import settings

class Token(models.Model):
    token_id = models.IntegerField(unique=True, default=0)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    volume_24h = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    volume_change_24h = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    percent_change_1h = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percent_change_24h = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percent_change_7d = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    market_cap_dominance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fully_diluted_market_cap = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    last_updated = models.DateTimeField()


    def __str__(self):
        return f"{self.name} ({self.symbol})"

class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'token')

    def __str__(self):
        return f"{self.user.username} - {self.token.symbol}"