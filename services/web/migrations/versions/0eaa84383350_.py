"""empty message

Revision ID: 0eaa84383350
Revises: 23db8c9b1dfa
Create Date: 2020-04-26 17:16:52.947128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eaa84383350'
down_revision = '23db8c9b1dfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pm_id', sa.Integer(), nullable=True),
    sa.Column('isEmpty', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['pm_id'], ['post_machines.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('post_machines', sa.Column('numbox', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_machines', 'numbox')
    op.drop_table('cells')
    # ### end Alembic commands ###
