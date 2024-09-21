# api/tests/test_views.py
import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from ninja.testing import TestAsyncClient
from api.views import api
from api.models import Stock, Order
from ninja_jwt.tokens import RefreshToken
from decimal import Decimal

@pytest.fixture
def auth_client(client, user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return client

@pytest.fixture
def stock(db):
    stock = Stock.objects.create(name='TestStock', price=Decimal('100.00'))
    return stock

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_place_order(auth_client, stock):
    payload = {
        "stock_id": stock.id,
        "quantity": 10,
        "order_type": "buy"
    }
    response = await auth_client.post("/orders/order", json=payload)
    assert response.status_code == 200
    assert response.json()['success'] == True
    order_id = response.json()['order_id']
    order = sync_to_async(Order.objects.get)(id=order_id)
    assert order.user.username == 'testuser'
    assert order.stock == stock
    assert order.quantity == 10
    assert order.order_type == 'buy'

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_total_investment(auth_client, user, stock):
    await sync_to_async(Order.objects.create)(user=user, stock=stock, quantity=10, order_type='buy')
    await sync_to_async(Order.objects.create)(user=user, stock=stock, quantity=5, order_type='sell')
    response = await auth_client.get(f"/orders/total/{stock.id}")
    assert response.status_code == 200
    total_investment = response.json()['total_investment']
    assert total_investment == 500  # (10*100) - (5*100)


@pytest.mark.asyncio
async def test_place_order_unauthorized(client, stock):
    payload = {
        "stock_id": stock.id,
        "quantity": 10,
        "order_type": "buy"
    }
    response = await client.post("/orders/order", json=payload)
    assert response.status_code == 401  # Unauthorized
