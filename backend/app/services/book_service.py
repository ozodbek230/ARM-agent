# [Fayl maqsadi: Kitoblar biznes mantiqi qatlami (Service)]
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.exceptions import NotFoundError
from backend.app.models.book import Book
from backend.app.repositories.book_repo import BookRepository, book_repo
from backend.app.schemas.book import BookCreate, BookListResponse, BookUpdate


class BookService:
    """Kitoblar domeni biznes mantiqi xizmati."""

    def __init__(self, repository: BookRepository | None = None) -> None:
        self.repo = repository or book_repo

    async def get_book_by_id(self, db: AsyncSession, book_id: int) -> Book:
        """ID bo'yicha kitobni olish, topilmasa NotFoundError tashlash."""
        book = await self.repo.get_by_id(db, book_id)
        if book is None:
            raise NotFoundError(detail="Kitob topilmadi")
        return book

    async def get_books(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> BookListResponse:
        """Kitoblar ro'yxatini pagination bilan olish."""
        items, total = await self.repo.get_all(db, skip=skip, limit=limit)
        return BookListResponse(items=items, total=total, skip=skip, limit=limit)

    async def create_book(self, db: AsyncSession, book_in: BookCreate) -> Book:
        """Yangi kitob yaratish."""
        return await self.repo.create(db, book_in)

    async def update_book(
        self, db: AsyncSession, book_id: int, book_in: BookUpdate
    ) -> Book:
        """Mavjud kitob ma'lumotlarini yangilash."""
        book = await self.get_book_by_id(db, book_id)
        update_data = book_in.model_dump(exclude_unset=True)
        return await self.repo.update(db, book, update_data)

    async def delete_book(self, db: AsyncSession, book_id: int) -> None:
        """Kitobni o'chirish."""
        book = await self.get_book_by_id(db, book_id)
        await self.repo.delete(db, book)


book_service = BookService()
