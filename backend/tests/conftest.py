# [Fayl maqsadi: Pytest global sozlamalari va fixturalari]
import pytest


@pytest.fixture(autouse=True)
async def cleanup_test_data():
    """Testlar tugagach, testlar davomida qo'shilgan vaqtinchalik yozuvlarni tozalash (idempotentlik uchun)."""
    yield
    from sqlalchemy import delete
    from backend.app.db.session import AsyncSessionLocal
    from backend.app.models.user import User

    async with AsyncSessionLocal() as session:
        stmt = delete(User).where(User.username.not_in(["admin", "talaba"]))
        await session.execute(stmt)
        await session.commit()
