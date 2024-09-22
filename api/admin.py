from django.contrib import admin
from .models import Order, Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
