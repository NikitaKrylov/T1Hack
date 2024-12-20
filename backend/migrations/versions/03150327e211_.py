"""empty message

Revision ID: 03150327e211
Revises: 
Create Date: 2024-11-16 06:13:50.345691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03150327e211'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('sprint_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('priority', sa.String(), nullable=True),
    sa.Column('ticket_number', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('parent_ticket_id', sa.Integer(), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('rank', sa.String(), nullable=True),
    sa.Column('estimation', sa.Integer(), nullable=True),
    sa.Column('workgroup', sa.String(), nullable=True),
    sa.Column('resolution', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entities_id'), 'entities', ['id'], unique=False)
    op.create_table('entities_changing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.Column('property_name', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('change_type', sa.String(), nullable=False),
    sa.Column('changed_from', sa.String(), nullable=True),
    sa.Column('changed_to', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entities_changing_id'), 'entities_changing', ['id'], unique=False)
    op.create_index(op.f('ix_entities_changing_property_name'), 'entities_changing', ['property_name'], unique=False)
    op.create_table('sprints',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sprint_status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=False),
    sa.Column('finished_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sprints_id'), 'sprints', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_sprints_id'), table_name='sprints')
    op.drop_table('sprints')
    op.drop_index(op.f('ix_entities_changing_property_name'), table_name='entities_changing')
    op.drop_index(op.f('ix_entities_changing_id'), table_name='entities_changing')
    op.drop_table('entities_changing')
    op.drop_index(op.f('ix_entities_id'), table_name='entities')
    op.drop_table('entities')
    # ### end Alembic commands ###
