"""Init

Revision ID: 61962eec31ce
Revises: e9e925e45f00
Create Date: 2023-04-22 15:18:42.150803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61962eec31ce'
down_revision = 'e9e925e45f00'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
