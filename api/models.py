from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    ORDER_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type.capitalize()} {self.quantity} of {self.stock.name}"
