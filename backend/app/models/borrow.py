# [Fayl maqsadi: Ijara (Borrow) va Bron (Reservation) SQLAlchemy modellari]
from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class BorrowStatus(str, PyEnum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class ReservationStatus(str, PyEnum):
    WAITING = "waiting"
    NOTIFIED = "notified"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True
    )
    borrow_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    returned_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=BorrowStatus.ACTIVE.value,
        nullable=False,
    )

    # Aloqalar (Relationships)
    user = relationship("User", backref="borrows", lazy="selectin")
    book = relationship("Book", backref="borrows", lazy="selectin")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reserved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    queue_position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=ReservationStatus.WAITING.value,
        nullable=False,
    )

    user = relationship("User", backref="reservations", lazy="selectin")
    book = relationship("Book", backref="reservations", lazy="selectin")
