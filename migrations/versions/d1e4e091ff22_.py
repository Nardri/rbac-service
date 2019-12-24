"""empty message

Revision ID: d1e4e091ff22
Revises: 175c2e6a95dc
Create Date: 2019-12-23 16:57:51.769265

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd1e4e091ff22'
down_revision = '175c2e6a95dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'permissions', ['id'])
    op.add_column('roles', sa.Column('is_default', sa.Boolean(),
                                     nullable=True))
    op.create_unique_constraint(None, 'roles', ['id'])
    op.create_unique_constraint(None, 'services', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'services', type_='unique')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_column('roles', 'is_default')
    op.drop_constraint(None, 'permissions', type_='unique')
    # ### end Alembic commands ###