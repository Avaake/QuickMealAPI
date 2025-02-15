from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR
from src.core import Base


class User(Base):
    first_name: Mapped[str] = mapped_column(VARCHAR(50))
    last_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_user: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_courier: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, is_active={self.is_active}, "
            f"is_user={self.is_user}), is_admin={self.is_admin}, "
            f"is_courier={self.is_courier}"
        )
