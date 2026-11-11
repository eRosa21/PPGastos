"""Vincula gastos aos usuários.

Revision ID: 7f2c9a1d4e60
Revises: 31e14fd56b4b
Create Date: 2026-11-11
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7f2c9a1d4e60"
down_revision: Union[str, Sequence[str], None] = "31e14fd56b4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("gastos", sa.Column("usuario", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "fk_gastos_usuario_usuarios",
        "gastos",
        "usuarios",
        ["usuario"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_gastos_usuario_usuarios", "gastos", type_="foreignkey")
    op.drop_column("gastos", "usuario")
