from src.schemas.order_schemas import OrderStatus
from src.core import Base
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Payment, User, OrderItem


class Order(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status_enum"),
        default=OrderStatus.pending,
        nullable=False,
    )
    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,  # якщо 1:1
    )

    payment: Mapped["Payment"] = relationship(
        "Payment", back_populates="order", uselist=False
    )
    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"user_id={self.user_id}, payment_id={self.payment_id})"
        )
