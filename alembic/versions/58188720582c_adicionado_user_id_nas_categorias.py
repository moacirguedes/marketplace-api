"""Adicionado user id nas categorias

Revision ID: 58188720582c
Revises: 2c4bd67570eb
Create Date: 2025-03-21 14:37:45.288989

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "58188720582c"
down_revision: Union[str, None] = "2c4bd67570eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "categories",
        sa.Column("user_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        None, "categories", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "categories", type_="foreignkey")
    op.drop_column("categories", "user_id")
    # ### end Alembic commands ###
