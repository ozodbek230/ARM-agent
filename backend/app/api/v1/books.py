# [Fayl maqsadi: Kitoblar domeni REST API endpointlari]
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.dependencies import check_role, get_current_admin, get_db
from backend.app.models.user import User
from backend.app.schemas.book import (
    BookCreate,
    BookFilterParams,
    BookListResponse,
    BookResponse,
    BookSearchResultResponse,
    BookUpdate,
)
from backend.app.schemas.common import MessageResponse
from backend.app.services.book_service import book_service

router = APIRouter()


@router.get(
    "",
    response_model=BookListResponse,
    summary="Kitoblar ro'yxatini olish (Pagination bilan)",
    description="Barcha foydalanuvchilar (mehmon, talaba, admin) uchun kitoblar ro'yxatini qaytaradi.",
)
async def get_books(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0, description="O'tkazib yuboriladigan yozuvlar soni"),
    limit: int = Query(20, ge=1, le=100, description="Qaytariladigan maksimal yozuvlar soni"),
) -> BookListResponse:
    """Kitoblar ro'yxatini pagination bilan qaytarish."""
    return await book_service.get_books(db, skip=skip, limit=limit)


@router.get(
    "/search",
    response_model=BookSearchResultResponse,
    summary="Kitoblarni qidirish va filtrlash",
    description="Nom, muallif, janr, holat va nashr yili bo'yicha qidiruv. Bo'sh natijada AI tavsiya beradi.",
)
async def search_books(
    db: Annotated[AsyncSession, Depends(get_db)],
    filters: Annotated[BookFilterParams, Depends()],
) -> BookSearchResultResponse:
    """Kitoblarni ko'p parametrli qidirish va filtrlash."""
    return await book_service.search_books(db, filters)


@router.get(
    "/genres",
    response_model=list[str],
    summary="Barcha mavjud janrlar ro'yxatini olish",
    description="Kutubxonadagi mavjud unikal janrlar ro'yxatini qaytaradi (Frontend filtrlari uchun).",
)
async def get_genres(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[str]:
    """Mavjud janrlar ro'yxatini qaytarish."""
    return await book_service.get_genres(db)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Bitta kitob haqida batafsil ma'lumot olish",
    description="ID bo'yicha kitob ma'lumotlarini qaytaradi. Barcha foydalanuvchilar uchun ochiq.",
)
async def get_book_by_id(
    book_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BookResponse:
    """Bitta kitobni ID bo'yicha qaytarish."""
    return await book_service.get_book_by_id(db, book_id)


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi kitob qo'shish",
    description="Faqat Administrator yoki Kutubxonachi (Librarian) yangi kitob qo'sha oladi.",
)
async def create_book(
    book_in: BookCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(check_role(["admin", "librarian"]))],
) -> BookResponse:
    """Yangi kitob qo'shish (Admin yoki Librarian)."""
    return await book_service.create_book(db, book_in)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Kitob ma'lumotlarini yangilash",
    description="Faqat Administrator yoki Kutubxonachi (Librarian) kitob ma'lumotlarini o'zgartira oladi.",
)
async def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(check_role(["admin", "librarian"]))],
) -> BookResponse:
    """Kitob ma'lumotlarini yangilash (Admin yoki Librarian)."""
    return await book_service.update_book(db, book_id, book_in)


@router.delete(
    "/{book_id}",
    response_model=MessageResponse,
    summary="Kitobni o'chirish",
    description="Faqat Bosh Administrator kitobni o'chirish huquqiga ega.",
)
async def delete_book(
    book_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: Annotated[User, Depends(get_current_admin)],
) -> MessageResponse:
    """Kitobni o'chirish (Faqat Admin)."""
    await book_service.delete_book(db, book_id)
    return MessageResponse(message="Kitob muvaffaqiyatli o'chirildi")
