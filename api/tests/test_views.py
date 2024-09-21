from asgiref.sync import sync_to_async
from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestAsyncClient
from ninja_jwt.tokens import RefreshToken
from twisted.protocols.amp import Decimal
from zope.interface.common import optional

from api.views import api
from api.models import Stock, Order
from datetime import datetime, timedelta
import jwt
from django.conf import settings

ninja_test_client = TestAsyncClient(api)

class TestAsyncViews(TestCase):
    def setUp(self):
        self.client = ninja_test_client
        # Create a test user
        self.user, _ = User.objects.get_or_create(username='testuser')
        self.user.save()
        # Create a test stock
        self.stock = Stock.objects.create(name='TestStock', price=100)
        # # Generate JWT token for authentication
        # payload = {
        #     'user_id': self.user.id,
        #     'exp': datetime.now() + timedelta(hours=24),
        #     'iat': datetime.now(),
        # }
        # self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # self.auth_header = {'Authorization': f'Bearer {self.token}'}
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    async def test_place_order(self):
        payload = {
            "stock_id": self.stock.id,
            "quantity": 10,
            "order_type": "buy"
        }
        response = await self.client.post("/orders/order", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        order_id = response.json()['order_id']
        # Verify the order exists in the database
        order = await sync_to_async(Order.objects.get)(id=order_id)
        self.assertEqual(order.user_id, self.user.id)
        self.assertEqual(order.stock_id, self.stock.id)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.order_type, 'buy')

    async def test_total_investment(self):
        # Create some orders
        await sync_to_async(Order.objects.create)(user=self.user, stock=self.stock, quantity=10, order_type='buy')
        await sync_to_async(Order.objects.create)(user=self.user, stock=self.stock, quantity=5, order_type='sell')
        response = await self.client.get(f"/orders/total/{self.stock.id}")
        self.assertEqual(response.status_code, 200)
        total_investment = response.json()['total_investment']
        self.assertEqual(float(total_investment), float(500))  # (10*100) - (5*100)

    async def test_invalid_token(self):
        # Use an invalid token
        invalid_auth_header = {'Authorization': 'Bearer invalidtoken'}
        payload = {
            "stock_id": self.stock.id,
            "quantity": 10,
            "order_type": "buy"
        }
        response = await self.client.post("/orders/order", json=payload, headers=invalid_auth_header)
        self.assertEqual(response.status_code, 401)
