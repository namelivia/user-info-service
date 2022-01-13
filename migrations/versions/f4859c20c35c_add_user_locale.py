"""add_user_locale

Revision ID: f4859c20c35c
Revises: 97f4c36233f0
Create Date: 2022-01-13 09:12:08.026672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4859c20c35c'
down_revision = '97f4c36233f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('locale', sa.String(), nullable=False, server_default="en"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.drop_column('locale')

    # ### end Alembic commands ###
