# [Fayl maqsadi: Kitoblar uchun Data Access Layer (Repository)]
from typing import Any
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.book import Book
from backend.app.schemas.book import BookCreate, BookFilterParams, BookUpdate


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

    async def search_and_filter(
        self, db: AsyncSession, filters: BookFilterParams
    ) -> tuple[list[Book], int]:
        """Kitoblarni ko'p parametrli qidirish, filtrlash, saralash va sahifalash."""
        conditions = []

        if filters.query and filters.query.strip():
            q_clean = filters.query.strip().lower()
            conditions.append(
                or_(
                    func.lower(Book.title).contains(q_clean),
                    func.lower(Book.author).contains(q_clean),
                )
            )

        if filters.genre and filters.genre.strip():
            conditions.append(func.lower(Book.genre).contains(filters.genre.strip().lower()))

        if filters.author and filters.author.strip():
            conditions.append(func.lower(Book.author).contains(filters.author.strip().lower()))

        if filters.status and filters.status.strip():
            conditions.append(Book.status == filters.status.strip().lower())

        if filters.year_from is not None:
            conditions.append(Book.year >= filters.year_from)

        if filters.year_to is not None:
            conditions.append(Book.year <= filters.year_to)

        # 1. Total count
        count_stmt = select(func.count()).select_from(Book)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_res = await db.execute(count_stmt)
        total = count_res.scalar() or 0

        # 2. Saralash (Sorting whitelist)
        allowed_sorts = {
            "id": Book.id,
            "title": Book.title,
            "year": Book.year,
            "created_at": Book.created_at,
        }
        sort_col = allowed_sorts.get(filters.sort_by.lower(), Book.id)
        order_by = sort_col.asc() if filters.order.lower() == "asc" else sort_col.desc()

        # 3. Natijalarni olish
        query_stmt = select(Book)
        if conditions:
            query_stmt = query_stmt.where(and_(*conditions))
        query_stmt = query_stmt.order_by(order_by).offset(filters.skip).limit(filters.limit)

        result = await db.execute(query_stmt)
        books = list(result.scalars().all())

        return books, total

    async def get_all_genres(self, db: AsyncSession) -> list[str]:
        """Bazadagi mavjud barcha unikal janrlar ro'yxatini qaytarish."""
        stmt = select(Book.genre).distinct().order_by(Book.genre.asc())
        result = await db.execute(stmt)
        return [row[0] for row in result.all() if row[0]]


book_repo = BookRepository()
