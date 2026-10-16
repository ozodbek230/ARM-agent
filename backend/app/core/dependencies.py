# [Fayl maqsadi: FastAPI Dependency Injection (DB sessiya, auth, rollar)]
from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.exceptions import ForbiddenError, UnauthorizedError
from backend.app.core.security import decode_token
from backend.app.db.session import AsyncSessionLocal
from backend.app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Har bir HTTP so'rovi uchun alohida AsyncSession taqdim etuvchi generator."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """JWT access tokenni tekshirib, joriy faol foydalanuvchini qaytaruvchi dependency."""
    try:
        payload = decode_token(token)
    except (JWTError, UnauthorizedError):
        raise UnauthorizedError(detail="Token yaroqsiz yoki muddati o'tgan")

    token_type = payload.get("type")
    if token_type != "access":
        raise UnauthorizedError(detail="Faqat access token qabul qilinadi")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedError(detail="Token ma'lumotlari yaroqsiz")

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedError(detail="Token identifikatori noto'g'ri formatda")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise UnauthorizedError(detail="Foydalanuvchi tizimda topilmadi")

    if not user.is_active:
        raise ForbiddenError(detail="Foydalanuvchi akkaunti faolsizlantirilgan")

    return user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Faqat administrator roliga ega foydalanuvchilarga ruxsat beruvchi dependency."""
    if current_user.role != UserRole.ADMIN and current_user.role != "admin":
        raise ForbiddenError(detail="Ushbu amal uchun administrator huquqi talab qilinadi")
    return current_user


def check_role(allowed_roles: list[str]):
    """Turli rollar (admin, librarian va boshqalar) uchun dinamik tekshiruvchi factory dependency."""
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenError(
                detail=f"Ushbu amal uchun ruxsat etilgan rollar: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker
