# [Fayl maqsadi: Ma'lumotlar bazasi ulanishi va sessiyalar boshqaruvi]
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from backend.app.core.config import settings
from backend.app.db.base import Base
# Barcha jadvallar Base.metadata da aks etishi uchun modellarni import qilamiz
import backend.app.models  # noqa: F401

is_sqlite = "sqlite" in settings.DATABASE_URL
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def create_tables() -> None:
    """Ma'lumotlar bazasida mavjud bo'lmagan jadvallarni yaratish (idempotent)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
