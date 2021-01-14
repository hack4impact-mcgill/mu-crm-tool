"""empty message

Revision ID: 16f7a241833d
Revises: 31a4cfc88ec7
Create Date: 2021-01-10 16:01:40.256054

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "16f7a241833d"
down_revision = "31a4cfc88ec7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "association",
        sa.Column("contact_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("contact_id", "project_id"),
    )
    op.drop_table("contacts")
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.create_table(
        "contacts",
        sa.Column("contact_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("project_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["contact_id"], ["contact.id"], name="contacts_contact_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="contacts_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("contact_id", "project_id", name="contacts_pkey"),
    )
    op.drop_table("association")
    # ### end Alembic commands ###