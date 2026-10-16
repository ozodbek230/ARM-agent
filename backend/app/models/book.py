# [Fayl maqsadi: Kitob (Book) SQLAlchemy modeli stubi - 2-agent uchun]
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base


class Book(Base):
    """Kitob modeli stubi. 2-agent (G'olib) ushbu modelni to'liq kengaytiradi."""
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
