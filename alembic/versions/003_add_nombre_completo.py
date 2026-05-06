"""Add nombre_completo to usuarios

Revision ID: 003_add_nombre_completo
Revises: 002_add_hashed_password
Create Date: 2026-05-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "003_add_nombre_completo"
down_revision: Union[str, None] = "002_add_hashed_password"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add nombre_completo column to usuarios table."""
    try:
        op.add_column(
            "usuarios",
            sa.Column("nombre_completo", sa.String(length=100), nullable=True),
        )
    except Exception:
        # Column already exists, skip
        pass


def downgrade() -> None:
    """Remove nombre_completo column from usuarios table."""
    try:
        op.drop_column("usuarios", "nombre_completo")
    except Exception:
        # Column doesn't exist, skip
        pass
