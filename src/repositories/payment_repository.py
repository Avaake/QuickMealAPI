from repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.enums import PaymentMethod
from core import Payment


class PaymentRepository(SQLAlchemyRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment, session)

    def create_instance(
        self, payment_method: PaymentMethod, total_price: int, paid: bool
    ) -> Payment:
        return self.model(
            method=payment_method,
            amount=total_price,
            paid=paid,
        )
