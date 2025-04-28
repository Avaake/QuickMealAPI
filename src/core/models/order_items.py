from core import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import Dish, Order


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int] = mapped_column()

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    dish: Mapped["Dish"] = relationship("Dish", back_populates="order_items")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"order_id={self.order_id}, dish_id={self.dish_id})"
        )
