"""expand_booking_status_enum

Revision ID: 53a4bdd3cb06
Revises: e8900cd23a36
Create Date: 2026-07-18

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "53a4bdd3cb06"
down_revision: Union[str, Sequence[str], None] = "e8900cd23a36"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'ASSIGNED';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'ACCEPTED';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'ON_THE_WAY';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'ARRIVED';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'WASHING';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'REJECTED';"
    )

    op.execute(
        "ALTER TYPE bookingstatus ADD VALUE IF NOT EXISTS 'NO_SHOW';"
    )


def downgrade() -> None:
    # PostgreSQL cannot remove enum values safely.
    pass