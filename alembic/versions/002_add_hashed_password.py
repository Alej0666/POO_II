"""Add hashed_password field to usuarios table

Revision ID: 002_add_hashed_password
Revises: 001_initial
Create Date: 2026-05-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002_add_hashed_password"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add hashed_password column to usuarios table."""
    # Add the hashed_password column with a default empty string
    op.add_column(
        "usuarios",
        sa.Column("hashed_password", sa.String(length=255), nullable=True, server_default=""),
    )
    # Then make it NOT NULL (after the default is applied)
    op.alter_column("usuarios", "hashed_password", nullable=False)


def downgrade() -> None:
    """Remove hashed_password column from usuarios table."""
    op.drop_column("usuarios", "hashed_password")
