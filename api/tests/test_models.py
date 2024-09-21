from decimal import Decimal

import pytest
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from api.models import Stock, Order


@pytest.mark.django_db
def test_stock_creation():
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    assert stock.name == 'TestStock'
    assert stock.price == Decimal('100.00')
    assert str(stock) == 'TestStock'

@pytest.mark.django_db
def test_order_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    order = Order.objects.create(
        user=user,
        stock=stock,
        quantity=10,
        order_type='buy'
    )
    assert order.user == user
    assert order.stock == stock
    assert order.quantity == 10
    assert order.order_type == 'buy'
    assert str(order) == 'Buy 10 of TestStock'
    assert order.value == 1000.00
    assert async_to_sync(stock.sum)(user) == 1000.00

@pytest.mark.django_db
def test_stock_sum():
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    order1 = Order.objects.create(
        user=user,
        stock=stock,
        quantity=10,
        order_type='buy'
    )
    order2 = Order.objects.create(
        user=user,
        stock=stock,
        quantity=10,
        order_type='sell'
    )
    order3 = Order.objects.create(
        user=user,
        stock=stock,
        quantity=4,
        order_type='buy'
    )
    order4 = Order.objects.create(
        user=user,
        stock=stock,
        quantity=6,
        order_type='buy'
    )

    assert async_to_sync(stock.sum)(user) == Decimal(1000)

@pytest.mark.django_db
def test_order_quantity_validation():
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    with pytest.raises(IntegrityError):
        Order.objects.create(
            user=user,
            stock=stock,
            quantity=-5,
            order_type='buy'
        )

@pytest.mark.django_db
def test_order_type_validation():
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    with pytest.raises(ValidationError):
        order = Order(
            user=user,
            stock=stock,
            quantity=10,
            order_type='invalid_type'
        )
        order.full_clean()
