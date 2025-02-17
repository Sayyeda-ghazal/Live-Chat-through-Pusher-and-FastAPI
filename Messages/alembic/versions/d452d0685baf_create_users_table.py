"""Create users table

Revision ID: d452d0685baf
Revises: ea2e439104a4
Create Date: 2025-02-13 15:02:01.827997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd452d0685baf'
down_revision: Union[str, None] = 'ea2e439104a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.alter_column('messages', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('messages_username_key', 'messages', type_='unique')
    op.create_foreign_key(None, 'messages', 'users', ['username'], ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_unique_constraint('messages_username_key', 'messages', ['username'])
    op.alter_column('messages', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('users')
    # ### end Alembic commands ###
