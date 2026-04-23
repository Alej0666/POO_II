"""Initial migration - create usuarios, proyectos, tareas tables.

Revision ID: 001_initial
Revises: 
Create Date: 2026-04-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create usuarios table
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )

    # Create proyectos table
    op.create_table(
        "proyectos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=500), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create tareas table
    op.create_table(
        "tareas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.String(length=500), nullable=True),
        sa.Column("prioridad", sa.Enum("ALTA", "MEDIA", "BAJA", name="prioridadtarea"), nullable=False, server_default="MEDIA"),
        sa.Column("estado", sa.Enum("pendiente", "en_progreso", "completada", name="estadotarea"), nullable=False, server_default="pendiente"),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["proyecto_id"], ["proyectos.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tareas")
    op.drop_table("proyectos")
    op.drop_table("usuarios")
