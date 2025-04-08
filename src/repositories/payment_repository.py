from src.repositories.sqlalchemy_repository import SQLAlchemyRepository, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from sqlalchemy.orm import selectinload
from typing import Union, Sequence
from src.core import Payment


class PaymentRepository(SQLAlchemyRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment, session)

    def create_instance(self, payment_method, total_price: int, paid: bool) -> Payment:
        return self.model(
            method=payment_method,
            amount=total_price,
            paid=paid,
        )
