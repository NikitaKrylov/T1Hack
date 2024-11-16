"""empty message

Revision ID: f8b3fb67c7e0
Revises: 70b997580c9b
Create Date: 2024-11-16 12:58:19.907032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8b3fb67c7e0'
down_revision: Union[str, None] = '70b997580c9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sprints', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_sprints_user_id'), 'sprints', ['user_id'], unique=False)
    op.create_foreign_key(None, 'sprints', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sprints', type_='foreignkey')
    op.drop_index(op.f('ix_sprints_user_id'), table_name='sprints')
    op.drop_column('sprints', 'user_id')
    # ### end Alembic commands ###