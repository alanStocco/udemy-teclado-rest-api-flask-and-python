"""empty message

Revision ID: 798ff009f9f7
Revises: 83a3da08d821
Create Date: 2023-11-13 17:00:51.168211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '798ff009f9f7'
down_revision = '83a3da08d821'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
