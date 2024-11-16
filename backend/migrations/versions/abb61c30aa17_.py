"""empty message

Revision ID: abb61c30aa17
Revises: 38464ceef12c
Create Date: 2024-11-16 11:37:43.476348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abb61c30aa17'
down_revision: Union[str, None] = '38464ceef12c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entities_changing', sa.Column('history_change', sa.String(), nullable=True))
    op.drop_column('entities_changing', 'changed_to')
    op.drop_column('entities_changing', 'changed_from')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entities_changing', sa.Column('changed_from', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('entities_changing', sa.Column('changed_to', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('entities_changing', 'history_change')
    # ### end Alembic commands ###
