from schemas.enums import PaymentMethod
from src.schemas.base_schema import BaseSchema

from src.core import Payment, OrderItem


class CreateOrderSchema(BaseSchema):
    payment_method: PaymentMethod


class AddCreatedOrderSchema(BaseSchema):
    user_id: int
    payment: "Payment"
    items: list["OrderItem"]

    model_config = {"arbitrary_types_allowed": True}
