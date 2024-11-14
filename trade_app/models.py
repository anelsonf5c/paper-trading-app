# models.py
from django.db import models
from django.contrib.auth.models import User

class Instrument(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.symbol

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=4)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.instrument.symbol} by {self.user.username}"
