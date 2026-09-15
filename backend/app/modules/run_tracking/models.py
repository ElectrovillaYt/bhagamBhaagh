
import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.shared.constants import WGS84_SRID
from app.shared.enums import RunStatus


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    distance: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[RunStatus] = mapped_column(
        Enum(RunStatus, name="run_status"),
        nullable=False,
        default=RunStatus.ACTIVE,
    )

    user: Mapped["User"] = relationship(
        back_populates="runs",
    )

    gps_points: Mapped[list["GPSPoint"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
        order_by="GPSPoint.timestamp",
    )

    route: Mapped["Route | None"] = relationship(
        back_populates="run",
        uselist=False,
        cascade="all, delete-orphan",
    )

    territory: Mapped["Territory | None"] = relationship(
        back_populates="run",
        uselist=False,
        cascade="all, delete-orphan",
    )


class GPSPoint(Base):
    __tablename__ = "gps_points"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=WGS84_SRID,
        ),
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    accuracy: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    run: Mapped["Run"] = relationship(
        back_populates="gps_points",
    )
