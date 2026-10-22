# [Fayl maqsadi: Ijara va bron uchun Data Access Layer (Repository)]
from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.borrow import Borrow, BorrowStatus, Reservation, ReservationStatus


class BorrowRepository:
    """Ijara va bron ma'lumotlar bazasi amallari (Data Access Layer)."""

    # ─── BORROW ────────────────────────────────────────────────────────────────

    async def get_borrow_by_id(self, db: AsyncSession, borrow_id: int) -> Borrow | None:
        """ID bo'yicha ijara yozuvini olish."""
        result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
        return result.scalar_one_or_none()

    async def get_active_borrow_by_book(self, db: AsyncSession, book_id: int) -> Borrow | None:
        """Kitob bo'yicha faol (qaytarilmagan) ijara yozuvini olish."""
        result = await db.execute(
            select(Borrow).where(
                and_(Borrow.book_id == book_id, Borrow.status == BorrowStatus.ACTIVE.value)
            )
        )
        return result.scalar_one_or_none()

    async def get_user_borrows(
        self, db: AsyncSession, user_id: int, active_only: bool = False
    ) -> list[Borrow]:
        """Foydalanuvchi ijaralarini olish (ixtiyoriy: faqat faollarini)."""
        stmt = select(Borrow).where(Borrow.user_id == user_id)
        if active_only:
            stmt = stmt.where(Borrow.status == BorrowStatus.ACTIVE.value)
        stmt = stmt.order_by(Borrow.borrow_date.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_overdue_borrows(self, db: AsyncSession) -> list[Borrow]:
        """Muddati o'tgan va hali qaytarilmagan ijaralar ro'yxatini qaytarish."""
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(Borrow).where(
                and_(
                    Borrow.due_date < now,
                    Borrow.returned_date.is_(None),
                    Borrow.status == BorrowStatus.ACTIVE.value,
                )
            )
        )
        return list(result.scalars().all())

    async def create_borrow(
        self, db: AsyncSession, user_id: int, book_id: int, days: int = 14
    ) -> Borrow:
        """Yangi ijara yozuvini bazaga qo'shish."""
        now = datetime.now(timezone.utc)
        db_borrow = Borrow(
            user_id=user_id,
            book_id=book_id,
            borrow_date=now,
            due_date=now + timedelta(days=days),
            status=BorrowStatus.ACTIVE.value,
        )
        db.add(db_borrow)
        await db.flush()
        await db.refresh(db_borrow)
        return db_borrow

    async def mark_as_returned(self, db: AsyncSession, borrow: Borrow) -> Borrow:
        """Ijarani qaytarilgan deb belgilash."""
        borrow.returned_date = datetime.now(timezone.utc)
        borrow.status = BorrowStatus.RETURNED.value
        await db.flush()
        await db.refresh(borrow)
        return borrow

    # ─── RESERVATION ───────────────────────────────────────────────────────────

    async def get_book_reservations(
        self, db: AsyncSession, book_id: int, active_only: bool = True
    ) -> list[Reservation]:
        """Kitob uchun bronlar ro'yxatini olish."""
        stmt = select(Reservation).where(Reservation.book_id == book_id)
        if active_only:
            stmt = stmt.where(
                Reservation.status.in_(
                    [ReservationStatus.WAITING.value, ReservationStatus.NOTIFIED.value]
                )
            )
        stmt = stmt.order_by(Reservation.queue_position.asc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_user_reservation_for_book(
        self, db: AsyncSession, user_id: int, book_id: int
    ) -> Reservation | None:
        """Foydalanuvchining muayyan kitob uchun faol bron yozuvini olish."""
        result = await db.execute(
            select(Reservation).where(
                and_(
                    Reservation.user_id == user_id,
                    Reservation.book_id == book_id,
                    Reservation.status.in_(
                        [ReservationStatus.WAITING.value, ReservationStatus.NOTIFIED.value]
                    ),
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_user_reservations(
        self, db: AsyncSession, user_id: int
    ) -> list[Reservation]:
        """Foydalanuvchining barcha bronlari ro'yxatini olish."""
        result = await db.execute(
            select(Reservation)
            .where(Reservation.user_id == user_id)
            .order_by(Reservation.reserved_at.desc())
        )
        return list(result.scalars().all())

    async def get_reservation_by_id(
        self, db: AsyncSession, reservation_id: int
    ) -> Reservation | None:
        """ID bo'yicha bron yozuvini olish."""
        result = await db.execute(
            select(Reservation).where(Reservation.id == reservation_id)
        )
        return result.scalar_one_or_none()

    async def create_reservation(
        self, db: AsyncSession, user_id: int, book_id: int, queue_position: int
    ) -> Reservation:
        """Yangi bron yozuvini bazaga qo'shish."""
        db_reservation = Reservation(
            user_id=user_id,
            book_id=book_id,
            queue_position=queue_position,
            status=ReservationStatus.WAITING.value,
        )
        db.add(db_reservation)
        await db.flush()
        await db.refresh(db_reservation)
        return db_reservation

    async def cancel_reservation(
        self, db: AsyncSession, reservation: Reservation
    ) -> None:
        """Bronni bekor qilish (status = 'cancelled')."""
        reservation.status = ReservationStatus.CANCELLED.value
        await db.flush()

    async def shift_queue_positions(
        self, db: AsyncSession, book_id: int, from_position: int
    ) -> None:
        """from_position dan katta bo'lgan barcha faol bronlar navbat o'rnini 1 ta kamaytirish."""
        await db.execute(
            update(Reservation)
            .where(
                and_(
                    Reservation.book_id == book_id,
                    Reservation.queue_position > from_position,
                    Reservation.status.in_(
                        [ReservationStatus.WAITING.value, ReservationStatus.NOTIFIED.value]
                    ),
                )
            )
            .values(queue_position=Reservation.queue_position - 1)
        )


borrow_repo = BorrowRepository()
