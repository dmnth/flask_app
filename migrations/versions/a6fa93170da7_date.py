"""date

Revision ID: a6fa93170da7
Revises: 0867c02a8d82
Create Date: 2021-11-05 16:15:57.834272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6fa93170da7'
down_revision = '0867c02a8d82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('date_added', sa.DateTime(), nullable=True))
    op.drop_index('ix_activities_date', table_name='activities')
    op.create_index(op.f('ix_activities_date_added'), 'activities', ['date_added'], unique=False)
    op.drop_column('activities', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('date', sa.DATETIME(), nullable=True))
    op.drop_index(op.f('ix_activities_date_added'), table_name='activities')
    op.create_index('ix_activities_date', 'activities', ['date'], unique=False)
    op.drop_column('activities', 'date_added')
    # ### end Alembic commands ###
