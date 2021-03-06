"""empty message

Revision ID: 622357fc3bda
Revises: 
Create Date: 2022-06-07 18:45:31.651085

"""
import sqlalchemy as sa
from alembic import op
from db.models import TSVector

# revision identifiers, used by Alembic.
revision = "622357fc3bda"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "breeds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column(
            "__ts_vector__",
            TSVector(),
            sa.Computed("to_tsvector('russian', coalesce(name,''))", persisted=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_breed___ts_vector__",
        "breeds",
        ["__ts_vector__"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "kitties",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("breed_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("image", sa.String(length=100), nullable=True),
        sa.Column("birthday", sa.Date(), nullable=False),
        sa.Column(
            "__ts_vector__",
            TSVector(),
            sa.Computed(
                "to_tsvector('russian', coalesce(name,'') || ' ' || coalesce(description,''))",
                persisted=True,
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["breed_id"], ["breeds.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_kitty___ts_vector__",
        "kitties",
        ["__ts_vector__"],
        unique=False,
        postgresql_using="gin",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_kitty___ts_vector__", table_name="kitties", postgresql_using="gin"
    )
    op.drop_table("kitties")
    op.drop_index("ix_breed___ts_vector__", table_name="breeds", postgresql_using="gin")
    op.drop_table("breeds")
    # ### end Alembic commands ###
