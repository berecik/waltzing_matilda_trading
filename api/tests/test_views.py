# api/tests/test_views.py
import pytest
from django.contrib.auth.models import User
from ninja import NinjaAPI
from httpx import AsyncClient
from django.urls import reverse
from asgiref.sync import sync_to_async
from api.models import Stock, Order
from api.views import api as ninja_api

@pytest.fixture
def api_client():
    from ninja.testing import TestClient
    return TestClient(ninja_api)

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_place_order(api_client):
    # Create a test user and authenticate
    user = await sync_to_async(User.objects.create_user)(
        username='testuser', password='testpass'
    )
    stock = await sync_to_async(Stock.objects.create)(
        name='TestStock', price=100
    )
    # Authenticate the client
    api_client.client.login(username='testuser', password='testpass')
    # Prepare the payload
    payload = {
        "stock_id": stock.id,
        "quantity": 10,
        "order_type": "buy"
    }
    # Send the request
    response = await api_client.post("/orders/order", payload)
    # Check the response
    assert response.status_code == 200
    assert response.json()['success'] == True
    order_id = response.json()['order_id']
    # Verify the order was created
    order = await sync_to_async(Order.objects.get)(id=order_id)
    assert order.user == user
    assert order.stock == stock
    assert order.quantity == 10
    assert order.order_type == 'buy'

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_total_investment(api_client):
    # Create a test user and authenticate
    user = await sync_to_async(User.objects.create_user)(
        username='testuser', password='testpass'
    )
    stock = await sync_to_async(Stock.objects.create)(
        name='TestStock', price=100
    )
    # Create orders
    await sync_to_async(Order.objects.create)(
        user=user, stock=stock, quantity=10, order_type='buy'
    )
    await sync_to_async(Order.objects.create)(
        user=user, stock=stock, quantity=5, order_type='sell'
    )
    # Authenticate the client
    api_client.client.login(username='testuser', password='testpass')
    # Send the request
    response = await api_client.get(f"/orders/total/{stock.id}")
    # Check the response
    assert response.status_code == 200
    total_investment = response.json()['total_investment']
    assert total_investment == 500  # (10*100) - (5*100)
