"""Added users, routes, runs, gps_points and territories table

Revision ID: 820931603a1a
Revises:
Create Date: 2026-09-15 21:12:16.751702

"""


from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    run_status_enum = postgresql.ENUM(
        "ACTIVE", "COMPLETED", "INVALID", "CANCELLED", name="run_status"
    )
    run_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("distance", sa.Float(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "ACTIVE", "COMPLETED", "INVALID", "CANCELLED", name="run_status", create_type=False
            ),
            nullable=False,
        ),
    )
    op.create_index("ix_runs_user_id", "runs", ["user_id"])

    op.create_table(
        "gps_points",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.Geography(geometry_type="POINT", srid=4326),
            nullable=False,
        ),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accuracy", sa.Float(), nullable=False),
    )
    op.create_index("ix_gps_points_run_id", "gps_points", ["run_id"])

    op.create_table(
        "routes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("runs.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "path",
            geoalchemy2.Geography(geometry_type="LINESTRING", srid=4326),
            nullable=False,
        ),
        sa.Column("distance", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_routes_run_id", "routes", ["run_id"], unique=True)

    op.create_table(
        "territories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("runs.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "polygon",
            geoalchemy2.Geography(geometry_type="POLYGON", srid=4326),
            nullable=False,
        ),
        sa.Column("area", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_territories_user_id", "territories", ["user_id"])
    op.create_index("ix_territories_run_id", "territories", ["run_id"], unique=True)

    # Spatial index — essential for the overlap check (ST_Intersects) to
    # scale beyond a handful of territories.
    op.execute(
        "CREATE INDEX ix_territories_polygon_gist ON territories USING GIST (polygon)"
    )


def downgrade() -> None:
    op.drop_index("ix_territories_polygon_gist", table_name="territories")
    op.drop_table("territories")
    op.drop_table("routes")
    op.drop_table("gps_points")
    op.drop_table("runs")
    op.execute("DROP TYPE run_status")
    op.drop_table("users")
