"""create order item tables

Revision ID: 795c2634ddf6
Revises: 8843577b890e
Create Date: 2025-04-07 21:13:09.873380

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "795c2634ddf6"
down_revision: Union[str, None] = "8843577b890e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"], ["dishes.id"], name=op.f("fk_order_items_dish_id_dishes")
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], name=op.f("fk_order_items_order_id_orders")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order_items")),
    )


def downgrade() -> None:
    op.drop_table("order_items")
