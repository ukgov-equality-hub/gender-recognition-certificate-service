"""empty message

Revision ID: 6adf7ebb3032
Revises: b8e628c72cd0
Create Date: 2023-01-05 11:20:09.722282

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '6adf7ebb3032'
down_revision = 'b8e628c72cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('last_page', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application', 'last_page')
    # ### end Alembic commands ###