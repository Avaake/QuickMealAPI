from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, TEXT
from src.core import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Dish


class Category(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)

    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="category")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}"
