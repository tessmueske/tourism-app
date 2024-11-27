"""updated models for profile info

Revision ID: 1cb7342ee1e0
Revises: b3f3bc3cbebc
Create Date: 2024-11-27 13:22:33.398981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb7342ee1e0'
down_revision = 'b3f3bc3cbebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))

    with op.batch_alter_table('localexperts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))

    with op.batch_alter_table('travelers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('travelers', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('bio')
        batch_op.drop_column('age')
        batch_op.drop_column('name')

    with op.batch_alter_table('localexperts', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('bio')
        batch_op.drop_column('age')
        batch_op.drop_column('name')

    with op.batch_alter_table('advertisers', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('bio')
        batch_op.drop_column('age')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
