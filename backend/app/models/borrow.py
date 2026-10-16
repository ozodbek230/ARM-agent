# [Fayl maqsadi: Ijara va bron (Borrow) SQLAlchemy modeli stubi - 4-agent uchun]
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base


class Borrow(Base):
    """Ijara modeli stubi. 4-agent (Navro'zbek) ushbu modelni to'liq kengaytiradi."""
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
