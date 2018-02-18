"""empty message

Revision ID: 7d82391d648d
Revises: 
Create Date: 2018-02-18 17:34:30.983904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d82391d648d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('shoppinglists')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('shoppinglists',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('shoppinglists_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('desc', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('date_added', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='shoppinglists_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='shoppinglists_pkey'),
    sa.UniqueConstraint('user_id', 'name', name='unq_b_name'),
    postgresql_ignore_search_path=False
    )
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=5), autoincrement=False, nullable=True),
    sa.Column('date_added', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('shoppinglist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['shoppinglist_id'], ['shoppinglists.id'], name='items_shoppinglist_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='items_pkey'),
    sa.UniqueConstraint('shoppinglist_id', 'name', name='unq_i_name')
    )
    # ### end Alembic commands ###
