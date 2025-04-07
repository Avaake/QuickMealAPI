from src.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.schemas.order_schemas import PaymentMethod
from sqlalchemy import ForeignKey, Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Order


class Payment(Base):

    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method_enum"), nullable=False
    )
    amount: Mapped[int] = mapped_column(nullable=False, default=0)
    paid: Mapped[bool] = mapped_column(default=False, nullable=False)

    order: Mapped["Order"] = relationship(
        "Order", back_populates="payment", uselist=False
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"method={self.method}, paid={self.paid})"
        )
