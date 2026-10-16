bu jamoaviy ema balki bitta odam qiladi, men o'zim, buni sal soddalashtir va 7 ta AI agent ishlashi uchun toliq prompt yozib ber, biri baza yana biri boshqa ish hullas toliq ish jarayonini tuz, har bir agent ketma ket ishlaydi parallel emas, haar birining ishi keyingisiga bogliq boladi har biri ishlagandan keyin o'zidan olidngi yozilgan kodga moslaydi, har biri o'zi uchun  ham reja tuzadi, talablarni aniqlaydi, kelib chiqishi mumkin bolgan muammolarni oldindan yozib olib kodda u hatolarga yol qoyilishini oldini oladi, kod sodda qisqa va optimal yozadi, oxirida har biri necha fayl, necha qator kod yozganini qisqacha hisobot berib boradi, hozir faqat 1-agent uchun yoz, promptlar nomli papka ochhib 1-agent ishi deb nomlangan md yoki json faylga ishini yoz, oldin uni loyihani toliq organib chiqishini ham yoz



Bosqich	Nima qiladi
0 — O'rganish	26 ta faylni tartibda o'qiydi, bog'liqliklarni tushunadi
1 — Reja	Talablarni aniqlaydi + 7 ta muammoni oldindan yozib yechim topadi
2 — Kod	16 ta faylni to'ldiradi (config, security, db, models, schemas, api, main)
3 — Tekshirish	Import, mantiq va ishga tushirishni tekshiradi
4 — Hisobot	Har bir fayl/qator soni + 2-agent uchun eslatma
1-agent nima qiladi:
core/ — config, security, dependencies, exceptions
db/ — session, base, seed (admin akkaunt)
models/ — User to'liq + Book/Borrow stub
schemas/ — auth, user, common
api/v1/ — auth endpoints + router
main.py — FastAPI app
Keyingi agentlar uchun reja (taxminiy):

2-agent → Kitoblar (Book model, CRUD)
3-agent → Qidiruv & Filtr
4-agent → Ijara & Bron (Borrow)
5-agent → AI Agent
6-agent → Frontend (Kiosk + Web)
7-agent → Testlar va hujjat









Sen **ARM (Axborot Resurs Markazi)** loyihasining **birinchi va asosiy agenti** san. 
Keyingi barcha agentlar (2–7) **sening yozgan kodingga** tayanadi.
Sening ishingdagi har qanday xato butun loyihaga ta'sir qiladi — ehtiyotkor va aniq ishlash shart.

---

## 📋 BOSQICH 0: LOYIHANI O'RGANISH (MAJBURIY, KODDAN OLDIN)

Kod yozishdan oldin quyidagi barcha fayllarni o'qib, tushunib ol:

### O'qiladigan fayllar (tartibda):
1. `README.md` — loyiha maqsadi va ishga tushirish
2. `docs/README.md` — arxitektura va papkalar tuzilmasi
3. `.env.example` — barcha muhit o'zgaruvchilari
4. `requirements.txt` — mavjud paketlar
5. `backend/app/main.py` — asosiy kirish nuqtasi (bo'sh)
6. `backend/app/core/__init__.py`
7. `backend/app/core/config.py` — (bo'sh, sen to'ldirasan)
8. `backend/app/core/security.py` — (bo'sh, sen to'ldirasan)
9. `backend/app/core/dependencies.py` — (bo'sh, sen to'ldirasan)
10. `backend/app/core/exceptions.py` — (bo'sh, sen to'ldirasan)
11. `backend/app/db/__init__.py`
12. `backend/app/db/session.py` — (bo'sh, sen to'ldirasan)
13. `backend/app/db/base.py` — (bo'sh, sen to'ldirasan)
14. `backend/app/db/seed.py` — (bo'sh, sen to'ldirasan)
15. `backend/app/models/__init__.py`
16. `backend/app/models/user.py` — (bo'sh, sen to'ldirasan)
17. `backend/app/models/book.py` — (bo'sh, sen to'ldirasan — faqat stub)
18. `backend/app/models/borrow.py` — (bo'sh, sen to'ldirasan — faqat stub)
19. `backend/app/schemas/__init__.py`
20. `backend/app/schemas/auth.py` — (bo'sh, sen to'ldirasan)
21. `backend/app/schemas/user.py` — (bo'sh, sen to'ldirasan)
22. `backend/app/schemas/common.py` — (bo'sh, sen to'ldirasan)
23. `backend/app/api/__init__.py`
24. `backend/app/api/v1/__init__.py`
25. `backend/app/api/v1/router.py` — (bo'sh, sen to'ldirasan)
26. `backend/app/api/v1/auth.py` — (bo'sh, sen to'ldirasan)

### O'rganib bo'lgach o'zingga savol ber:
- Barcha fayllar qanday bog'langan?
- Qaysi fayl qaysi faylga import qiladi?
- Import sikli (circular import) xavfi bormi?
- Keyingi agentlar (kitoblar, ijara, AI) qanday modullar kutadi?

---

## 🎯 SENING VAZIFANG

Sen quyidagi **5 ta asosiy qatlam**ni to'liq yozasan:

| # | Modul | Fayllar |
|---|---|---|
| 1 | **Sozlamalar** | `core/config.py` |
| 2 | **Xavfsizlik & Auth** | `core/security.py`, `core/dependencies.py`, `core/exceptions.py` |
| 3 | **Ma'lumotlar bazasi** | `db/session.py`, `db/base.py`, `db/seed.py` |
| 4 | **Modellar & Sxemalar** | `models/user.py`, `models/book.py`(stub), `models/borrow.py`(stub), `schemas/auth.py`, `schemas/user.py`, `schemas/common.py` |
| 5 | **Auth API & Asosiy App** | `api/v1/auth.py`, `api/v1/router.py`, `main.py` |

---

## 📐 BOSQICH 1: REJA TUZISH (KODDAN OLDIN YOZILADI)

Reja tuzishdan oldin quyidagi savollarni o'zingga bering va yozib qo'y:

### 1.1 Talablarni aniqlash
- `User` modelida qanday maydonlar kerak?
- Kutubxona tizimida kim admin, kim oddiy foydalanuvchi?
- JWT token qanday ishlashi kerak (access + refresh)?
- Seed data nima bo'lishi kerak (admin akkaunt)?
- `book.py` va `borrow.py` stub qanday ko'rinishda bo'lishi kerak (2-agent uchun)?

### 1.2 Kelib chiqishi mumkin bo'lgan muammolar (oldindan yoz)
Har bir muammoni va uning yechimini quyida ko'rsatilgan formatda **kod yozishdan oldin** yozib qo'y:

```
MUAMMO: SQLAlchemy async session va sync kod aralashishi
YECHIM: Barcha DB amallari uchun faqat async def ishlatiladi,
        get_db dependency faqat AsyncSession qaytaradi
```

```
MUAMMO: Circular import — models/base.py va models/user.py
YECHIM: Base class db/base.py da e'lon qilinadi,
        models/__init__.py da barcha modellar import qilinadi
        db/base.py esa modellarni import qilmaydi
```

```
MUAMMO: bcrypt va passlib versiya muvofiqligi
YECHIM: requirements.txt dagi passlib[bcrypt]==1.7.4 versiyasida
        CryptContext(schemes=["bcrypt"]) ishlatiladi
```

```
MUAMMO: aiosqlite bilan SQLite WAL mode
YECHIM: engine yaratishda connect_args={"check_same_thread": False}
        va pool_pre_ping=True ishlatiladi
```

```
MUAMMO: Token muddati o'tganda 401 o'rniga 500 xatosi
YECHIM: dependencies.py da JWTError try/except bilan ushlash,
        har doim HTTPException(401) qaytarish
```

```
MUAMMO: Seed data har safar ishga tushganda qayta qo'shilishi
YECHIM: seed() funksiyasi avval adminni qidiradi,
        mavjud bo'lsa o'tkazib yuboradi (idempotent)
```

```
MUAMMO: CORS settings hardcode qilinishi
YECHIM: Barcha CORS, SECRET_KEY, DB_URL .env dan o'qiladi,
        .env.example da default qiymatlar ko'rsatilgan
```

### 1.3 Fayl bo'yicha reja
Har bir fayl uchun nima yozishni oldindan belgilab ol:

```
core/config.py      → Settings class (pydantic-settings), .env o'qish
core/security.py    → hash_password, verify_password, create_token, decode_token
core/dependencies.py→ get_db, get_current_user, get_current_admin
core/exceptions.py  → NotFoundError, UnauthorizedError, ForbiddenError, BadRequestError

db/session.py       → AsyncEngine, AsyncSessionLocal, create_tables() funksiya
db/base.py          → DeclarativeBase (Base class) — modellarni import etadi
db/seed.py          → seed_admin() async funksiya

models/user.py      → User(Base): id, email, username, hashed_password, role, is_active, created_at
models/book.py      → Book(Base): stub — faqat id va __tablename__
models/borrow.py    → Borrow(Base): stub — faqat id va __tablename__

schemas/auth.py     → LoginRequest, TokenResponse, RefreshRequest
schemas/user.py     → UserCreate, UserResponse, UserUpdate
schemas/common.py   → PaginationParams, MessageResponse, ErrorResponse

api/v1/auth.py      → POST /login, POST /refresh, GET /me
api/v1/router.py    → barcha v1 routerlarni birlashtiradi (hozircha faqat auth)
main.py             → FastAPI app, CORS, lifespan (DB init + seed), router ulash
```

---

## 💻 BOSQICH 2: KOD YOZISH QOIDALARI

### Umumiy qoidalar:
1. **Sodda va qisqa** — bitta funksiya bitta ish qiladi
2. **Type hint** — barcha funksiyalarda
3. **Docstring** — faqat murakkab mantiq uchun (har biriga emas)
4. **Hardcode yo'q** — barcha config `.env` dan
5. **Import tartibi**: stdlib → third-party → local
6. **Har bir faylning tepasida** qisqa izoh: `# [Fayl maqsadi]`

### Xato boshqaruv qoidasi:
```python
# TO'G'RI:
raise HTTPException(status_code=404, detail="Kitob topilmadi")

# NOTO'G'RI:
return {"error": "not found"}
```

### Async qoidasi:
```python
# TO'G'RI — barcha DB amallari async:
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# NOTO'G'RI — sync:
def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()
```

---

## 📦 KOD SHABLONLARI (QISMAN)

### `core/config.py` ko'rinishi:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ARM"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite+aiosqlite:///./arm.db"
    BACKEND_CORS_ORIGINS: list[str] = []

    class Config:
        env_file = ".env"

settings = Settings()
```

### `models/user.py` ko'rinishi:
```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime, timezone
from enum import Enum as PyEnum
from backend.app.db.base import Base

class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
```

### `main.py` ko'rinishi (lifespan pattern):
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.db.session import create_tables
from backend.app.db.seed import seed_admin
from backend.app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await seed_admin()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, ...)
app.include_router(api_router, prefix=settings.API_V1_STR)
```

---

## ✅ BOSQICH 3: TEKSHIRISH

Kod yozib bo'lgach, quyidagi tekshiruvlarni o'tka:

### 3.1 Import tekshiruvi
- [ ] Circular import yo'qmi? (models → db/base, db/base → models emas)
- [ ] Barcha `__init__.py` fayllar to'g'ri import qiladimi?

### 3.2 Mantiq tekshiruvi
- [ ] `seed_admin()` ikki marta chaqirilganda xato bermaydimi?
- [ ] JWT decode xatosi 401 qaytaradimi?
- [ ] Admin dependency oddiy user uchun 403 qaytaradimi?
- [ ] `create_tables()` allaqachon mavjud jadvalni yo'q qilmaydimi?

### 3.3 Ishga tushirish
```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
# http://127.0.0.1:8000/docs → /auth/login endpoint ko'rinishi kerak
# /auth/login ga admin@arm.uz / admin123 bilan kirish ishlashi kerak
```

---

## 📊 BOSQICH 4: HISOBOT (OXIRIDA YOZILADI)

Barcha ish tugagandan so'ng quyidagi formatda hisobot yoz:

```
## 1-AGENT HISOBOTI

### Yozilgan fayllar:
| Fayl | Qator soni | Holat |
|------|------------|-------|
| backend/app/main.py | XX | ✅ |
| backend/app/core/config.py | XX | ✅ |
| backend/app/core/security.py | XX | ✅ |
| backend/app/core/dependencies.py | XX | ✅ |
| backend/app/core/exceptions.py | XX | ✅ |
| backend/app/db/session.py | XX | ✅ |
| backend/app/db/base.py | XX | ✅ |
| backend/app/db/seed.py | XX | ✅ |
| backend/app/models/user.py | XX | ✅ |
| backend/app/models/book.py | XX | ✅ stub |
| backend/app/models/borrow.py | XX | ✅ stub |
| backend/app/schemas/auth.py | XX | ✅ |
| backend/app/schemas/user.py | XX | ✅ |
| backend/app/schemas/common.py | XX | ✅ |
| backend/app/api/v1/auth.py | XX | ✅ |
| backend/app/api/v1/router.py | XX | ✅ |
| JAMI | ~XXX | |

### 2-agent uchun eslatma:
- `User` modeli: `backend.app.models.user.User`
- `Base` class: `backend.app.db.base.Base`
- `AsyncSession`: `backend.app.db.session.AsyncSessionLocal`
- `get_db` dependency: `backend.app.core.dependencies.get_db`
- `get_current_user`: `backend.app.core.dependencies.get_current_user`
- `Book` modeli stub holida — sen `__tablename__ = "books"` dan boshlab to'ldirasan
```

---

## ⚠️ MUHIM ESLATMALAR

1. **`main.py` bo'sh qoldirma** — bu butun ilovaning kirish nuqtasi
2. **Stub fayllar (book.py, borrow.py)** — faqat `Base` dan meros oladigan bo'sh class yoz
3. **`.env` faylini yaratma** — foydalanuvchi o'zi `cp .env.example .env` qiladi
4. **Parolni tekis saqlab qo'yma** — faqat `hashed_password`
5. **Seed admin**: email=`admin@arm.uz`, username=`admin`, password=`admin123`

---

*Seni keyingi 2-agent kutmoqda. U sening `Book` stub modelingga,
`Base`, `get_db` va `get_current_user` dependency-laringga tayanadi.*
