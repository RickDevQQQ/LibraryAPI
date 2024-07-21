"""Добавил is_deleted

Revision ID: 3b73adf707a5
Revises: 9a205730f5fa
Create Date: 2024-07-21 22:29:36.463704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b73adf707a5'
down_revision: Union[str, None] = '9a205730f5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('genre', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('user', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_deleted')
    op.drop_column('genre', 'is_deleted')
    op.drop_column('book', 'is_deleted')
    # ### end Alembic commands ###
