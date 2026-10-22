# [Fayl maqsadi: API v1 routerlarini birlashtirish]
from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.books import router as books_router
from backend.app.api.v1.borrows import router as borrows_router

api_router = APIRouter()

# 1-agent: Autentifikatsiya va avtorizatsiya routeri
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# 2-agent: Kitoblar domeni (Books Core) routeri
api_router.include_router(books_router, prefix="/books", tags=["Books"])

# 4-agent: Ijara va Bron domeni routeri
api_router.include_router(borrows_router, prefix="/borrows", tags=["Borrows & Reservations"])
