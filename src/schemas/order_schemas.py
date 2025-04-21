from schemas.enums import PaymentMethod, OrderStatus
from src.schemas.base_schema import BaseSchema

from src.core import Payment, OrderItem


class CreateOrderSchema(BaseSchema):
    payment_method: PaymentMethod


class AddCreatedOrderSchema(BaseSchema):
    user_id: int
    payment: "Payment"
    items: list["OrderItem"]

    model_config = {"arbitrary_types_allowed": True}


class UpdateOrderSchema(BaseSchema):
    status: OrderStatus


class ReadOrderSchema(BaseSchema):
    user_id: int
    status: "OrderStatus"
    payment_id: int
