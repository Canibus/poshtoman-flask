"""empty message

Revision ID: 23db8c9b1dfa
Revises: d2b4a3b35cbd
Create Date: 2020-04-26 14:49:43.924891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23db8c9b1dfa'
down_revision = 'd2b4a3b35cbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_machines', 'isEmpty')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_machines', sa.Column('isEmpty', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
