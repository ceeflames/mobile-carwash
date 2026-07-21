"""add washer availability

Revision ID: 43e4b10dc745
Revises: 53a4bdd3cb06
Create Date: 2026-07-21 19:27:53.927734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '43e4b10dc745'
down_revision: Union[str, Sequence[str], None] = '53a4bdd3cb06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    washer_availability = postgresql.ENUM(
        "AVAILABLE",
        "BUSY",
        "OFFLINE",
        "ON_BREAK",
        name="washeravailability",
    )

    washer_availability.create(op.get_bind())

    op.add_column(
        "users",
        sa.Column(
            "availability",
            washer_availability,
            nullable=False,
            server_default="OFFLINE",
        ),
    )

def downgrade():

    op.drop_column(
        "users",
        "availability",
    )

    washer_availability = postgresql.ENUM(
        "AVAILABLE",
        "BUSY",
        "OFFLINE",
        "ON_BREAK",
        name="washeravailability",
    )

    washer_availability.drop(op.get_bind())