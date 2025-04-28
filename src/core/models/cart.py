from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from core import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import Dish, User


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    user: Mapped["User"] = relationship("User", back_populates="cart_items")
    dish: Mapped["Dish"] = relationship("Dish", back_populates="items")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, "
            f"dish_id={self.dish_id}, quantity={self.quantity})"
        )
