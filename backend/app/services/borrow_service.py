# [Fayl maqsadi: Ijara va bron biznes mantiq qatlami (Service)]
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from backend.app.models.borrow import ReservationStatus
from backend.app.models.user import User
from backend.app.repositories.book_repo import book_repo
from backend.app.repositories.borrow_repo import borrow_repo
from backend.app.schemas.borrow import (
    BorrowCreate,
    BorrowListResponse,
    BorrowResponse,
    ReservationCreate,
    ReservationListResponse,
    ReservationResponse,
    ReturnRequest,
)
from backend.app.schemas.common import MessageResponse


class BorrowService:
    """Ijara va bron biznes mantiqlarini boshqaruvchi servis qatlami."""

    # ─── BORROW ────────────────────────────────────────────────────────────────

    async def borrow_book(
        self, db: AsyncSession, user_id: int, borrow_in: BorrowCreate
    ) -> BorrowResponse:
        """Kitobni ijaraga olish."""
        book = await book_repo.get_by_id(db, borrow_in.book_id)
        if not book:
            raise NotFoundError(detail="Kitob topilmadi")

        if book.status != "available":
            raise BadRequestError(
                detail="Kitob hozirda band. Faqat bron (navbat) qilishingiz mumkin."
            )

        borrow = await borrow_repo.create_borrow(
            db, user_id=user_id, book_id=borrow_in.book_id, days=borrow_in.days
        )

        book.status = "borrowed"
        await db.commit()
        await db.refresh(borrow)

        return BorrowResponse.model_validate(borrow)

    async def return_book(
        self, db: AsyncSession, current_user: User, return_in: ReturnRequest
    ) -> BorrowResponse:
        """Kitobni qaytarish."""
        borrow = None
        if return_in.borrow_id:
            borrow = await borrow_repo.get_borrow_by_id(db, return_in.borrow_id)
        elif return_in.book_id:
            borrow = await borrow_repo.get_active_borrow_by_book(db, return_in.book_id)

        if not borrow:
            raise NotFoundError(detail="Ijara yozuvi topilmadi")

        if borrow.status == "returned":
            raise BadRequestError(detail="Ushbu kitob allaqachon qaytarilgan")

        user_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
        if user_role not in ("admin", "librarian"):
            if borrow.user_id != current_user.id:
                raise ForbiddenError(
                    detail="Faqat o'zingiz olgan kitobni qaytarishingiz mumkin"
                )

        book = await book_repo.get_by_id(db, borrow.book_id)
        borrow = await borrow_repo.mark_as_returned(db, borrow)

        if book:
            active_reservations = await borrow_repo.get_book_reservations(
                db, book.id, active_only=True
            )
            waiting = [
                r for r in active_reservations
                if r.status == ReservationStatus.WAITING.value
            ]
            if waiting:
                first_in_queue = min(waiting, key=lambda r: r.queue_position)
                first_in_queue.status = ReservationStatus.NOTIFIED.value
                book.status = "reserved"
            else:
                book.status = "available"

        await db.commit()
        await db.refresh(borrow)
        return BorrowResponse.model_validate(borrow)

    async def get_my_borrows(
        self, db: AsyncSession, user_id: int
    ) -> BorrowListResponse:
        """Joriy foydalanuvchining barcha ijaralari."""
        borrows = await borrow_repo.get_user_borrows(db, user_id)
        return BorrowListResponse(
            items=[BorrowResponse.model_validate(b) for b in borrows],
            total=len(borrows),
        )

    async def get_overdue_borrows(self, db: AsyncSession) -> BorrowListResponse:
        """Muddati o'tgan ijaralar (Admin/Librarian uchun)."""
        borrows = await borrow_repo.get_overdue_borrows(db)
        return BorrowListResponse(
            items=[BorrowResponse.model_validate(b) for b in borrows],
            total=len(borrows),
        )

    # ─── RESERVATION ───────────────────────────────────────────────────────────

    async def reserve_book(
        self, db: AsyncSession, user_id: int, reserve_in: ReservationCreate
    ) -> ReservationResponse:
        """Kitobga navbatga yozilish."""
        book = await book_repo.get_by_id(db, reserve_in.book_id)
        if not book:
            raise NotFoundError(detail="Kitob topilmadi")

        if book.status == "available":
            raise BadRequestError(
                detail="Kitob hozirda bo'sh, uni to'g'ridan-to'g'ri ijaraga olishingiz mumkin."
            )

        existing = await borrow_repo.get_user_reservation_for_book(
            db, user_id, reserve_in.book_id
        )
        if existing:
            raise BadRequestError(
                detail="Siz allaqachon ushbu kitob uchun navbatga yozilgansiz."
            )

        active_reservations = await borrow_repo.get_book_reservations(
            db, reserve_in.book_id, active_only=True
        )
        if len(active_reservations) >= 3:
            raise BadRequestError(
                detail="Ushbu kitob uchun navbat to'lgan (maksimal 3 kishi)."
            )

        queue_position = len(active_reservations) + 1
        reservation = await borrow_repo.create_reservation(
            db, user_id=user_id, book_id=reserve_in.book_id, queue_position=queue_position
        )
        await db.commit()
        await db.refresh(reservation)
        return ReservationResponse.model_validate(reservation)

    async def cancel_reservation(
        self, db: AsyncSession, current_user: User, reservation_id: int
    ) -> MessageResponse:
        """Bronni bekor qilish."""
        reservation = await borrow_repo.get_reservation_by_id(db, reservation_id)
        if not reservation:
            raise NotFoundError(detail="Bron topilmadi")

        user_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
        if user_role not in ("admin", "librarian"):
            if reservation.user_id != current_user.id:
                raise ForbiddenError(
                    detail="Faqat o'zingizning broningizni bekor qilishingiz mumkin"
                )

        cancelled_position = reservation.queue_position
        was_notified = reservation.status == ReservationStatus.NOTIFIED.value
        book_id = reservation.book_id

        await borrow_repo.cancel_reservation(db, reservation)
        await borrow_repo.shift_queue_positions(db, book_id, cancelled_position)

        if was_notified:
            updated_reservations = await borrow_repo.get_book_reservations(
                db, book_id, active_only=True
            )
            waiting = [
                r for r in updated_reservations
                if r.status == ReservationStatus.WAITING.value
            ]
            if waiting:
                first_in_queue = min(waiting, key=lambda r: r.queue_position)
                first_in_queue.status = ReservationStatus.NOTIFIED.value
            else:
                book = await book_repo.get_by_id(db, book_id)
                if book and book.status == "reserved":
                    book.status = "available"

        await db.commit()
        return MessageResponse(message="Bron muvaffaqiyatli bekor qilindi")

    async def get_my_reservations(
        self, db: AsyncSession, user_id: int
    ) -> ReservationListResponse:
        """Joriy foydalanuvchining barcha bronlari."""
        reservations = await borrow_repo.get_user_reservations(db, user_id)
        return ReservationListResponse(
            items=[ReservationResponse.model_validate(r) for r in reservations],
            total=len(reservations),
        )


borrow_service = BorrowService()
