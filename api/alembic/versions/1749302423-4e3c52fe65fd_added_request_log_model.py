"""Added request log model

Revision ID: 4e3c52fe65fd
Revises: b633ed550e2c
Create Date: 2025-06-07 13:20:23.424450+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e3c52fe65fd"
down_revision: Union[str, None] = "b633ed550e2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "request_logs",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("client_ip", sa.VARCHAR(length=45), nullable=False),
        sa.Column("method", sa.VARCHAR(length=10), nullable=False),
        sa.Column("path", sa.VARCHAR(length=255), nullable=False),
        sa.Column(
            "query_params", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "request_header", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "request_body", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("response_status", sa.INTEGER(), nullable=False),
        sa.Column(
            "response_header", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "response_body", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("duration_ms", sa.REAL(), nullable=False),
        sa.Column("error", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_request_logs_client_ip"), "request_logs", ["client_ip"], unique=False
    )
    op.create_index(
        op.f("ix_request_logs_created_at"), "request_logs", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_request_logs_path"), "request_logs", ["path"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_request_logs_path"), table_name="request_logs")
    op.drop_index(op.f("ix_request_logs_created_at"), table_name="request_logs")
    op.drop_index(op.f("ix_request_logs_client_ip"), table_name="request_logs")
    op.drop_table("request_logs")
    # ### end Alembic commands ###
