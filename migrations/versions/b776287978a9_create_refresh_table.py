"""create refresh table

Revision ID: b776287978a9
Revises: 6dfad9f9077a
Create Date: 2022-10-01 22:21:18.853540

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b776287978a9"
down_revision = "6dfad9f9077a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "refresh_token",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column("key", sa.String(255), nullable=False),
        sa.Column("valid_until", sa.Float(), nullable=False),
        sa.Column("user_id", sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )


def downgrade():
    op.drop_table("refresh_token")
