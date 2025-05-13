from schemas.enums import PaymentMethod, OrderStatus
from schemas.base_schema import BaseSchema
from core import Payment, OrderItem


class PaymentShema(BaseSchema):
    id: int
    method: str
    amount: int
    paid: bool


class OrderItemSchema(BaseSchema):
    order_id: int
    dish_id: int
    quantity: int
    price: int


class CreateOrderSchema(BaseSchema):
    payment_method: PaymentMethod


class AddCreatedOrderInstanceSchema(BaseSchema):
    user_id: int
    payment: "Payment"
    items: list["OrderItem"]

    model_config = {"arbitrary_types_allowed": True}


class UpdateOrderSchema(BaseSchema):
    status: OrderStatus


class ReadOrderSchema(BaseSchema):
    user_id: int
    status: "OrderStatus"
    payment: PaymentShema
    items: list[OrderItemSchema]
