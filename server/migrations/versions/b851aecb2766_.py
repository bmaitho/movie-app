"""empty message

Revision ID: b851aecb2766
Revises: cbbb2a573be7
Create Date: 2024-07-16 07:25:19.059110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b851aecb2766'
down_revision = 'cbbb2a573be7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_link', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('poster_link')

    # ### end Alembic commands ###
