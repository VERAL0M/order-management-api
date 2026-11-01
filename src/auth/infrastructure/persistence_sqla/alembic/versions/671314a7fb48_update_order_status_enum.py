"""update order status enum

Revision ID: 671314a7fb48
Revises: 3ebafd10b117
Create Date: 2026-11-01 10:19:25.715871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '671314a7fb48'
down_revision: Union[str, None] = '3ebafd10b117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE order_status RENAME VALUE 'cancelled' TO 'canceled'"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TYPE order_status RENAME VALUE 'canceled' TO 'cancelled'"
    )