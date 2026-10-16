# [Fayl maqsadi: DB moduli eksportlari]
from backend.app.db.base import Base
from backend.app.db.session import AsyncSessionLocal, create_tables, engine
from backend.app.db.seed import seed_admin

__all__ = ["Base", "engine", "AsyncSessionLocal", "create_tables", "seed_admin"]
