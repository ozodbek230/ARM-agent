# [Fayl maqsadi: API v1 routerlarini birlashtirish]
from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router

api_router = APIRouter()

# 1-agent: Autentifikatsiya va avtorizatsiya routeri
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
