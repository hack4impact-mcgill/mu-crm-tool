"""added_by from optional to must

Revision ID: 7b6603edc867
Revises: ffc022de0771
Create Date: 2021-05-08 19:18:24.871196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7b6603edc867"
down_revision = "ffc022de0771"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "donations", "added_by", existing_type=postgresql.UUID(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "donations", "added_by", existing_type=postgresql.UUID(), nullable=True
    )
    # ### end Alembic commands ###