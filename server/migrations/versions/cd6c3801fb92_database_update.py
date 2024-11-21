"""database update

Revision ID: cd6c3801fb92
Revises: 
Create Date: 2024-11-21 17:03:36.145376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6c3801fb92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advertisers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('islands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('localexperts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('bio', sa.String(), nullable=False),
    sa.Column('areas_of_expertise', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('travelers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('advertiser_activity',
    sa.Column('advertiser_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name=op.f('fk_advertiser_activity_activity_id_activities')),
    sa.ForeignKeyConstraint(['advertiser_id'], ['advertisers.id'], name=op.f('fk_advertiser_activity_advertiser_id_advertisers')),
    sa.PrimaryKeyConstraint('advertiser_id', 'activity_id')
    )
    op.create_table('advertiser_island',
    sa.Column('advertiser_id', sa.Integer(), nullable=False),
    sa.Column('island_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['advertiser_id'], ['advertisers.id'], name=op.f('fk_advertiser_island_advertiser_id_advertisers')),
    sa.ForeignKeyConstraint(['island_id'], ['islands.id'], name=op.f('fk_advertiser_island_island_id_islands')),
    sa.PrimaryKeyConstraint('advertiser_id', 'island_id')
    )
    op.create_table('localexpert_activity',
    sa.Column('localexpert_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name=op.f('fk_localexpert_activity_activity_id_activities')),
    sa.ForeignKeyConstraint(['localexpert_id'], ['localexperts.id'], name=op.f('fk_localexpert_activity_localexpert_id_localexperts')),
    sa.PrimaryKeyConstraint('localexpert_id', 'activity_id')
    )
    op.create_table('localexpert_island',
    sa.Column('localexpert_id', sa.Integer(), nullable=False),
    sa.Column('island_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['island_id'], ['islands.id'], name=op.f('fk_localexpert_island_island_id_islands')),
    sa.ForeignKeyConstraint(['localexpert_id'], ['localexperts.id'], name=op.f('fk_localexpert_island_localexpert_id_localexperts')),
    sa.PrimaryKeyConstraint('localexpert_id', 'island_id')
    )
    op.create_table('traveler_activity',
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name=op.f('fk_traveler_activity_activity_id_activities')),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name=op.f('fk_traveler_activity_traveler_id_travelers')),
    sa.PrimaryKeyConstraint('traveler_id', 'activity_id')
    )
    op.create_table('traveler_advertiser',
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.Column('advertiser_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['advertiser_id'], ['advertisers.id'], name=op.f('fk_traveler_advertiser_advertiser_id_advertisers')),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name=op.f('fk_traveler_advertiser_traveler_id_travelers')),
    sa.PrimaryKeyConstraint('traveler_id', 'advertiser_id')
    )
    op.create_table('traveler_island',
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.Column('island_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['island_id'], ['islands.id'], name=op.f('fk_traveler_island_island_id_islands')),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name=op.f('fk_traveler_island_traveler_id_travelers')),
    sa.PrimaryKeyConstraint('traveler_id', 'island_id')
    )
    op.create_table('traveler_localexpert',
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.Column('localexpert_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['localexpert_id'], ['localexperts.id'], name=op.f('fk_traveler_localexpert_localexpert_id_localexperts')),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name=op.f('fk_traveler_localexpert_traveler_id_travelers')),
    sa.PrimaryKeyConstraint('traveler_id', 'localexpert_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traveler_localexpert')
    op.drop_table('traveler_island')
    op.drop_table('traveler_advertiser')
    op.drop_table('traveler_activity')
    op.drop_table('localexpert_island')
    op.drop_table('localexpert_activity')
    op.drop_table('advertiser_island')
    op.drop_table('advertiser_activity')
    op.drop_table('travelers')
    op.drop_table('localexperts')
    op.drop_table('islands')
    op.drop_table('advertisers')
    op.drop_table('activities')
    # ### end Alembic commands ###
