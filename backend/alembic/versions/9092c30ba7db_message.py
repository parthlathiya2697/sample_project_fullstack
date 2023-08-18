"""message

Revision ID: 9092c30ba7db
Revises: 5c89a726934c
Create Date: 2023-08-08 05:18:07.883416

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = '9092c30ba7db'
down_revision = '5c89a726934c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('name', sa.String(), nullable=True))
    op.add_column('items', sa.Column('notes', sa.String(), nullable=True))
    op.add_column('items', sa.Column('completed', sa.Boolean(), nullable=False))
    op.add_column('items', sa.Column('duration', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'duration')
    op.drop_column('items', 'completed')
    op.drop_column('items', 'notes')
    op.drop_column('items', 'name')
    # ### end Alembic commands ###