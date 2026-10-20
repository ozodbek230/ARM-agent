# [Fayl maqsadi: Kitoblar uchun Data Access Layer (Repository)]
from typing import Any
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.book import Book
from backend.app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    """Kitoblar ma'lumotlar bazasi amallari (Data Access Layer)."""

    async def get_by_id(self, db: AsyncSession, book_id: int) -> Book | None:
        """ID bo'yicha bitta kitobni olish."""
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> tuple[list[Book], int]:
        """Barcha kitoblar ro'yxatini pagination va jami soni bilan qaytarish."""
        count_result = await db.execute(select(func.count()).select_from(Book))
        total = count_result.scalar() or 0

        stmt = select(Book).order_by(Book.id.asc()).offset(skip).limit(limit)
        items_result = await db.execute(stmt)
        books = list(items_result.scalars().all())

        return books, total

    async def create(self, db: AsyncSession, obj_in: BookCreate) -> Book:
        """Yangi kitob yozuvini bazaga qo'shish."""
        book_data = obj_in.model_dump()
        db_obj = Book(**book_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: Book, update_data: dict[str, Any] | BookUpdate
    ) -> Book:
        """Mavjud kitob ma'lumotlarini yangilash."""
        if isinstance(update_data, dict):
            values = update_data
        else:
            values = update_data.model_dump(exclude_unset=True)

        for field, value in values.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: Book) -> None:
        """Kitobni bazadan o'chirish."""
        await db.delete(db_obj)
        await db.commit()


book_repo = BookRepository()
