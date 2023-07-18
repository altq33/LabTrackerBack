"""add tasks_count to subject model

Revision ID: 745a20b1a454
Revises: eb5ba852b13d
Create Date: 2023-07-18 16:28:05.775524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '745a20b1a454'
down_revision = 'eb5ba852b13d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('tasks_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subjects', 'tasks_count')
    # ### end Alembic commands ###
