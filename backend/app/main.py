# [Fayl maqsadi: ARM kutubxona tizimining asosiy kirish nuqtasi]
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.router import api_router
from backend.app.core.config import settings
from backend.app.db.seed import seed_admin
from backend.app.db.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ilova ishga tushganda jadvallarni yaratish va dastlabki ma'lumotlarni kiritish."""
    # 1. Baza jadvallarini avtomatik yaratish
    await create_tables()
    # 2. Dastlabki admin hisobini kiritish (idempotent)
    await seed_admin()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="ARM (Axborot Resurs Markazi) — Kutubxona boshqaruv tizimi va Kiosk/Web API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 routerini ulash
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
async def root():
    """Tizim holatini tekshirish uchun boshlang'ich endpoint."""
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Salomatlik tekshiruvi (Healthcheck)."""
    return {"status": "healthy"}
