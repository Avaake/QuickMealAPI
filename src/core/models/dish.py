from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey, TEXT, Integer
from src.core import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Category


class Dish(Base):
    __tablename__ = "dishes"
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="menu",
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, category_id={self.category_id})"
        )
