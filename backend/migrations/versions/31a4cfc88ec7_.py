"""empty message

Revision ID: 31a4cfc88ec7
Revises: 399ff7606b03
Create Date: 2021-01-10 15:54:43.671297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '31a4cfc88ec7'
down_revision = '399ff7606b03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_types',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('hex_colour', sa.String(length=8), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('province', sa.String(length=64), nullable=True),
    sa.Column('postal_code', sa.String(length=64), nullable=True),
    sa.Column('neighbourhood', sa.String(length=256), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('role')
    )
    op.create_table('contact',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('secondary_email', sa.String(length=256), nullable=True),
    sa.Column('cellphone', sa.String(length=256), nullable=False),
    sa.Column('role', sa.String(length=256), nullable=True),
    sa.Column('organization', sa.String(length=256), nullable=False),
    sa.Column('neighbourhood', sa.String(length=256), nullable=True),
    sa.Column('contact_type', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['contact_type'], ['contact_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('donations',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('donation_source', sa.String(length=128), nullable=False),
    sa.Column('event', sa.String(length=128), nullable=True),
    sa.Column('num_tickets', sa.Integer(), nullable=True),
    sa.Column('added_by', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('contacts',
    sa.Column('contact_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('contact_id', 'project_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    op.drop_table('donations')
    op.drop_table('contact')
    op.drop_table('users')
    op.drop_table('projects')
    op.drop_table('contact_types')
    # ### end Alembic commands ###
