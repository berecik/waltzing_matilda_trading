from functools import cached_property

from asgiref.sync import sync_to_async
from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def sells(self, user):
        return self.order_set.filter(order_type="sell", user=user)

    def buys(self, user):
        return self.order_set.filter(order_type="buy", user=user)

    async def sum(self, user):

        sell_set = await sync_to_async(self.sells)(user)
        sell = await sync_to_async(sell_set.aggregate)(sum=models.Sum("quantity"))

        buy_set = await sync_to_async(self.buys)(user)
        buy = await sync_to_async(buy_set.aggregate)(sum=models.Sum("quantity"))

        total = ((buy["sum"] or 0) - (sell["sum"] or 0)) * self.price

        return total

    def __str__(self):
        return self.name


class Order(models.Model):
    BUY = "buy"
    SELL = "sell"
    ORDER_TYPES = [
        (BUY, "Buy"),
        (SELL, "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    @cached_property
    def value(self):
        return self.quantity * self.stock.price

    def __str__(self):
        return f"{self.order_type.capitalize()} {self.quantity} of {self.stock.name}"
