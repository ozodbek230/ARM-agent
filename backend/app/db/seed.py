# [Fayl maqsadi: Boshlang'ich tizim ma'lumotlarini bazaga kiritish (seed data)]
from sqlalchemy import or_, select
from backend.app.core.security import hash_password
from backend.app.db.session import AsyncSessionLocal
from backend.app.models.user import User, UserRole


async def seed_admin() -> None:
    """Tizim birinchi marta ishga tushganda admin va test foydalanuvchini idempotent tarzda yaratish."""
    async with AsyncSessionLocal() as session:
        # 1. Admin tekshirish va yaratish
        admin_query = select(User).where(
            or_(User.email == "admin@arm.uz", User.username == "admin")
        )
        admin_result = await session.execute(admin_query)
        existing_admin = admin_result.scalar_one_or_none()

        if existing_admin is None:
            admin = User(
                email="admin@arm.uz",
                username="admin",
                full_name="Bosh Administrator",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            session.add(admin)

        # 2. Test talaba tekshirish va yaratish
        user_query = select(User).where(
            or_(User.email == "talaba@arm.uz", User.username == "talaba")
        )
        user_result = await session.execute(user_query)
        existing_user = user_result.scalar_one_or_none()

        if existing_user is None:
            student = User(
                email="talaba@arm.uz",
                username="talaba",
                full_name="Test Talaba",
                hashed_password=hash_password("talaba123"),
                role=UserRole.USER,
                is_active=True,
            )
            session.add(student)

        await session.commit()
