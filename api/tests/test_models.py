# api/tests/test_models.py
import pytest
from django.contrib.auth.models import User
from api.models import Stock, Order
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_stock_creation():
    # Create a stock
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    # Verify the stock was created
    assert stock.name == 'TestStock'
    assert stock.price == Decimal('100.00')
    # Verify __str__ method
    assert str(stock) == 'TestStock'

@pytest.mark.django_db
def test_stock_price_validation():
    with pytest.raises(ValidationError):
        stock = Stock(name='InvalidStock', price=Decimal('-50.00'))
        stock.full_clean()

@pytest.mark.django_db
def test_order_creation():
    # Create user and stock
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    # Create an order
    order = Order.objects.create(
        user=user,
        stock=stock,
        quantity=10,
        order_type='buy'
    )
    # Verify the order was created
    assert order.user == user
    assert order.stock == stock
    assert order.quantity == 10
    assert order.order_type == 'buy'
    # Verify __str__ method
    assert str(order) == 'Buy 10 of TestStock'

@pytest.mark.django_db
def test_order_quantity_validation():
    # Create user and stock
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    # Test negative quantity
    with pytest.raises(IntegrityError):
        Order.objects.create(
            user=user,
            stock=stock,
            quantity=-5,
            order_type='buy'
        )

@pytest.mark.django_db
def test_order_type_validation():
    # Create user and stock
    user = User.objects.create_user(username='testuser', password='testpass')
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    # Test invalid order type
    with pytest.raises(ValidationError):
        order = Order(
            user=user,
            stock=stock,
            quantity=10,
            order_type='invalid_type'
        )
        order.full_clean()
