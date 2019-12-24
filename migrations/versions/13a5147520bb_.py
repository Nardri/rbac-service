"""empty message

Revision ID: 13a5147520bb
Revises: d1e4e091ff22
Create Date: 2019-12-23 19:57:21.625493

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '13a5147520bb'
down_revision = 'd1e4e091ff22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services',
                  sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('services', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'services',
        sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('services', 'is_active')
    # ### end Alembic commands ###