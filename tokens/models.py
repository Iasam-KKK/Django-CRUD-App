# models.py
from django.db import models
from django.conf import settings

class Token(models.Model):
    token_id = models.IntegerField(unique=False, default=0)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    quote = models.JSONField(null=True, blank=True)  # Store detailed quote data
    last_updated = models.DateTimeField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserToken', related_name='tokens')

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.token.symbol}"