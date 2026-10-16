# [Fayl maqsadi: Autentifikatsiya API endpointlari (/login, /refresh, /me, /register)]
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.dependencies import get_current_user, get_db
from backend.app.core.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.app.models.user import User, UserRole
from backend.app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from backend.app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Tizimga kirish va tokenlar olish",
    description="Username yoki email hamda parol orqali autentifikatsiya qilinadi.",
)
async def login(
    login_data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Foydalanuvchi tizimga kirishi va access/refresh token olishi."""
    user_query = select(User).where(
        or_(
            User.email == login_data.username.strip(),
            User.username == login_data.username.strip(),
        )
    )
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedError(detail="Login yoki parol noto'g'ri")

    if not user.is_active:
        raise ForbiddenError(detail="Foydalanuvchi akkaunti faolsizlantirilgan")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Access tokenni yangilash",
    description="Yaroqli refresh token orqali yangi juftlikdagi tokenlarni olish.",
)
async def refresh_token(
    refresh_data: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Yangi access va refresh token yaratish."""
    try:
        payload = decode_token(refresh_data.refresh_token)
    except Exception:
        raise UnauthorizedError(detail="Refresh token yaroqsiz yoki muddati o'tgan")

    token_type = payload.get("type")
    if token_type != "refresh":
        raise UnauthorizedError(detail="Faqat refresh token qabul qilinadi")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedError(detail="Token ma'lumotlari yaroqsiz")

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedError(detail="Token identifikatori noto'g'ri formatda")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedError(detail="Foydalanuvchi tizimda topilmadi")

    if not user.is_active:
        raise ForbiddenError(detail="Foydalanuvchi akkaunti faolsizlantirilgan")

    new_access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Joriy foydalanuvchi profilini olish",
    description="Yuborilgan JWT Bearer token orqali tizimga kirgan foydalanuvchi ma'lumotlarini qaytaradi.",
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Joriy tizimga kirgan foydalanuvchi profilini qaytarish."""
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi foydalanuvchini ro'yxatdan o'tkazish",
    description="Yangi talaba yoki kitobxon profilini yaratadi.",
)
async def register(
    user_in: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """Yangi foydalanuvchi yaratish."""
    existing_query = select(User).where(
        or_(
            User.email == user_in.email.strip(),
            User.username == user_in.username.strip(),
        )
    )
    result = await db.execute(existing_query)
    if result.scalar_one_or_none():
        raise ConflictError(detail="Bunday email yoki username allaqachon ro'yxatdan o'tgan")

    new_user = User(
        email=user_in.email.strip(),
        username=user_in.username.strip(),
        full_name=user_in.full_name.strip() if user_in.full_name else None,
        hashed_password=hash_password(user_in.password),
        role=user_in.role or UserRole.USER,
        is_active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
