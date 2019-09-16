"""groups, challenges, group_challenges tables

Revision ID: ba2d05491b7a
Revises: 
Create Date: 2019-09-16 12:14:17.239102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba2d05491b7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('challenges',
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('max_score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('challenge_id')
    )
    op.create_table('groups',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=64), nullable=False),
    sa.Column('group_psw', sa.String(length=64), nullable=False),
    sa.Column('connected_users', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_index(op.f('ix_groups_group_name'), 'groups', ['group_name'], unique=True)
    op.create_table('challenge_group',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('n_attempts', sa.Integer(), nullable=True),
    sa.Column('best_score', sa.Integer(), nullable=True),
    sa.Column('last_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenges.challenge_id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.PrimaryKeyConstraint('group_id', 'challenge_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('challenge_group')
    op.drop_index(op.f('ix_groups_group_name'), table_name='groups')
    op.drop_table('groups')
    op.drop_table('challenges')
    # ### end Alembic commands ###