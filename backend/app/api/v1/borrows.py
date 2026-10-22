# [Fayl maqsadi: Ijara va bron REST API endpointlari]
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.dependencies import (
    check_role,
    get_current_user,
    get_db,
)
from backend.app.models.user import User
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
from backend.app.services.borrow_service import borrow_service

router = APIRouter()


@router.post(
    "",
    response_model=BorrowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Kitob olish (Borrow)",
    description="Foydalanuvchi tizimdan kitob ijaraga oladi. Kitob 'available' holatida bo'lishi shart.",
)
async def borrow_book(
    borrow_in: BorrowCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> BorrowResponse:
    return await borrow_service.borrow_book(db, current_user.id, borrow_in)


@router.post(
    "/return",
    response_model=BorrowResponse,
    status_code=status.HTTP_200_OK,
    summary="Kitob qaytarish (Return)",
    description="Foydalanuvchi ijaraga olgan kitobini qaytaradi. borrow_id yoki book_id orqali.",
)
async def return_book(
    return_in: ReturnRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> BorrowResponse:
    return await borrow_service.return_book(db, current_user, return_in)


@router.get(
    "/my",
    response_model=BorrowListResponse,
    status_code=status.HTTP_200_OK,
    summary="Mening kitoblarim",
    description="Joriy foydalanuvchining barcha faol va qaytarilgan ijaralari.",
)
async def get_my_borrows(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> BorrowListResponse:
    return await borrow_service.get_my_borrows(db, current_user.id)


@router.get(
    "/overdue",
    response_model=BorrowListResponse,
    status_code=status.HTTP_200_OK,
    summary="Muddati o'tgan kitoblar (Admin/Librarian)",
    description="Muddati o'tgan va qaytarilmagan barcha ijaralar ro'yxati.",
    dependencies=[Depends(check_role(["admin", "librarian"]))],
)
async def get_overdue_borrows(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BorrowListResponse:
    return await borrow_service.get_overdue_borrows(db)


@router.post(
    "/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Kitobga navbatga yozilish (Reserve)",
    description="Band kitob uchun foydalanuvchi navbatga yoziladi. Maksimal 3 ta odam.",
)
async def reserve_book(
    reserve_in: ReservationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ReservationResponse:
    return await borrow_service.reserve_book(db, current_user.id, reserve_in)


@router.get(
    "/reservations/my",
    response_model=ReservationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Mening bronlarim",
    description="Joriy foydalanuvchining barcha bron yozuvlari.",
)
async def get_my_reservations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ReservationListResponse:
    return await borrow_service.get_my_reservations(db, current_user.id)


@router.delete(
    "/reservations/{reservation_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Bronni bekor qilish (Cancel Reservation)",
    description="Foydalanuvchi o'z bronini bekor qiladi. Admin va Librarian ham bekor qila oladi.",
)
async def cancel_reservation(
    reservation_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    return await borrow_service.cancel_reservation(db, current_user, reservation_id)
