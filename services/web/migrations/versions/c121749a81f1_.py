"""empty message

Revision ID: c121749a81f1
Revises: 7fbccb135a09
Create Date: 2020-05-16 11:54:25.027358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c121749a81f1'
down_revision = '7fbccb135a09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cells')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cells',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pm_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('isEmpty', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='cells_order_id_fkey'),
    sa.ForeignKeyConstraint(['pm_id'], ['post_machines.id'], name='cells_pm_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='cells_pkey')
    )
    # ### end Alembic commands ###
