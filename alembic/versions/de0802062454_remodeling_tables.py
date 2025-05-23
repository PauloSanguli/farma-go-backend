"""remodeling tables

Revision ID: de0802062454
Revises:
Create Date: 2025-04-29 13:13:40.538038

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "de0802062454"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("basemodel")
    op.add_column(
        "medicine",
        sa.Column("stock_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.drop_constraint("medicine_pharmacy_id_fkey", "medicine", type_="foreignkey")
    op.create_foreign_key(None, "medicine", "stock", ["stock_id"], ["id"])
    op.drop_column("medicine", "stock")
    op.drop_column("medicine", "pharmacy_id")
    op.alter_column(
        "pharmacist",
        "password",
        existing_type=sa.VARCHAR(length=255),
        type_=sqlmodel.sql.sqltypes.AutoString(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "pharmacist",
        "email",
        existing_type=sa.VARCHAR(length=100),
        type_=sqlmodel.sql.sqltypes.AutoString(length=120),
        existing_nullable=False,
    )
    op.add_column(
        "pharmacy",
        sa.Column("stock_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.create_foreign_key(None, "pharmacy", "stock", ["stock_id"], ["id"])
    op.alter_column(
        "pharmacyimage",
        "image_url",
        existing_type=sa.VARCHAR(length=255),
        type_=sqlmodel.sql.sqltypes.AutoString(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "password",
        existing_type=sa.VARCHAR(length=255),
        type_=sqlmodel.sql.sqltypes.AutoString(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "email",
        existing_type=sa.VARCHAR(length=100),
        type_=sqlmodel.sql.sqltypes.AutoString(length=120),
        existing_nullable=False,
    )
    op.drop_column("user", "role")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.alter_column(
        "user",
        "email",
        existing_type=sqlmodel.sql.sqltypes.AutoString(length=120),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "password",
        existing_type=sqlmodel.sql.sqltypes.AutoString(length=500),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "pharmacyimage",
        "image_url",
        existing_type=sqlmodel.sql.sqltypes.AutoString(length=500),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.drop_constraint(None, "pharmacy", type_="foreignkey")
    op.drop_column("pharmacy", "stock_id")
    op.alter_column(
        "pharmacist",
        "email",
        existing_type=sqlmodel.sql.sqltypes.AutoString(length=120),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "pharmacist",
        "password",
        existing_type=sqlmodel.sql.sqltypes.AutoString(length=500),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.add_column(
        "medicine",
        sa.Column("pharmacy_id", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "medicine",
        sa.Column("stock", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "medicine", type_="foreignkey")
    op.create_foreign_key(
        "medicine_pharmacy_id_fkey", "medicine", "pharmacy", ["pharmacy_id"], ["id"]
    )
    op.drop_column("medicine", "stock_id")
    op.create_table(
        "basemodel",
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="basemodel_pkey"),
    )
    # ### end Alembic commands ###
