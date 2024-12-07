"""Removed Comment class

Revision ID: 7674a2f6830d
Revises: e10f3a39b54c
Create Date: 2024-12-07 21:13:46.161252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7674a2f6830d'
down_revision = 'e10f3a39b54c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traveler_comment')
    op.drop_table('advertiser_comment')
    op.drop_table('localexpert_comment')
    op.drop_table('comments')
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comments', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('comments')

    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('author', sa.VARCHAR(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('text', sa.VARCHAR(), nullable=False),
    sa.Column('traveler_id', sa.INTEGER(), nullable=True),
    sa.Column('localexpert_id', sa.INTEGER(), nullable=True),
    sa.Column('advertiser_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['advertiser_id'], ['advertisers.id'], name='fk_comments_advertiser_id_advertisers'),
    sa.ForeignKeyConstraint(['localexpert_id'], ['localexperts.id'], name='fk_comments_localexpert_id_localexperts'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_comments_post_id_posts'),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name='fk_comments_traveler_id_travelers'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('localexpert_comment',
    sa.Column('localexpert_id', sa.INTEGER(), nullable=False),
    sa.Column('comment_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name='fk_localexpert_comment_comment_id_comments'),
    sa.ForeignKeyConstraint(['localexpert_id'], ['localexperts.id'], name='fk_localexpert_comment_localexpert_id_localexperts'),
    sa.PrimaryKeyConstraint('localexpert_id', 'comment_id')
    )
    op.create_table('advertiser_comment',
    sa.Column('advertiser_id', sa.INTEGER(), nullable=False),
    sa.Column('comment_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['advertiser_id'], ['advertisers.id'], name='fk_advertiser_comment_advertiser_id_advertisers'),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name='fk_advertiser_comment_comment_id_comments'),
    sa.PrimaryKeyConstraint('advertiser_id', 'comment_id')
    )
    op.create_table('traveler_comment',
    sa.Column('traveler_id', sa.INTEGER(), nullable=False),
    sa.Column('comment_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name='fk_traveler_comment_comment_id_comments'),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name='fk_traveler_comment_traveler_id_travelers'),
    sa.PrimaryKeyConstraint('traveler_id', 'comment_id')
    )
    # ### end Alembic commands ###
