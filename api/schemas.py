from ninja import Schema
from decimal import Decimal


class OrderSchema(Schema):
    stock_id: int
    quantity: int
    order_type: str  # 'buy' or 'sell'


class StockInvestmentSchema(Schema):
    total_investment: Decimal
