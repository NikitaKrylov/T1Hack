"""empty message

Revision ID: 70b997580c9b
Revises: abb61c30aa17
Create Date: 2024-11-16 11:40:06.259038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '70b997580c9b'
down_revision: Union[str, None] = 'abb61c30aa17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entities_changing', 'entity_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('entities_changing', 'property_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('entities_changing', 'date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('entities_changing', 'version',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('entities_changing', 'change_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entities_changing', 'change_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('entities_changing', 'version',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('entities_changing', 'date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('entities_changing', 'property_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('entities_changing', 'entity_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
