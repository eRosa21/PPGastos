"""Renomeia as colunas de vínculo para usuario_id.

Revision ID: b48c7e21d963
Revises: 20943a930fcb
Create Date: 2026-11-11
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b48c7e21d963"
down_revision: Union[str, Sequence[str], None] = "20943a930fcb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "bancos",
        "usuario",
        new_column_name="usuario_id",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "gastos",
        "usuario",
        new_column_name="usuario_id",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "gastos",
        "usuario_id",
        new_column_name="usuario",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "bancos",
        "usuario_id",
        new_column_name="usuario",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
