"""empty message

Revision ID: de41806211bf
Revises: 178dec87dac7
Create Date: 2020-04-25 16:09:34.646263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de41806211bf'
down_revision = '178dec87dac7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_machines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isEmpty', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timeUp', sa.DateTime(), nullable=True),
    sa.Column('timeDowm', sa.DateTime(), nullable=True),
    sa.Column('courierId', sa.Integer(), nullable=True),
    sa.Column('postMachineId', sa.Integer(), nullable=True),
    sa.Column('clientPhone', sa.String(length=128), nullable=False),
    sa.Column('orderTime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['courierId'], ['couriers.id'], ),
    sa.ForeignKeyConstraint(['postMachineId'], ['post_machines.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('post_machines')
    # ### end Alembic commands ###
