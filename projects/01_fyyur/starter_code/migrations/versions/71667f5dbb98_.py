"""empty message

Revision ID: 71667f5dbb98
Revises: 2aa99a3a8325
Create Date: 2020-03-22 21:43:19.754064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71667f5dbb98'
down_revision = '2aa99a3a8325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genres', sa.PickleType(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.Text(), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'genres')
    # ### end Alembic commands ###
