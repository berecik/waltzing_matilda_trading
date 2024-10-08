from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import AsyncJWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from .models import Stock, Order
from .schemas import OrderSchema, StockInvestmentSchema

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

order_router = Router()


@order_router.post("/order", auth=AsyncJWTAuth())
async def place_order(request, payload: OrderSchema):
    user = request.auth
    stock = await sync_to_async(get_object_or_404)(Stock, id=payload.stock_id)
    order = Order(
        user=user,
        stock=stock,
        quantity=payload.quantity,
        order_type=payload.order_type,
    )
    await sync_to_async(order.save)()
    return {"success": True, "order_id": order.id}


@order_router.get("/total/{stock_id}", auth=AsyncJWTAuth())
async def total_investment(request, stock_id: int):
    user = request.auth
    stock = await sync_to_async(get_object_or_404)(Stock, id=stock_id)
    total = await stock.sum(user)
    return StockInvestmentSchema(total_investment=total)


api.add_router("/orders/", order_router)
