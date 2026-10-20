# 🤖 2-AGENT PROMPTI: KITOBLAR DOMENI (BOOKS CORE)

Sen **ARM (Axborot Resurs Markazi)** loyihasining **ikkinchi agenti** san (**Erkinov G'olib — Backend Kitoblar Domeni**).
1-agent loyihaning arxitekturaviy poydevori, ma'lumotlar bazasi, xavfsizlik va autentifikatsiya qatlamini to'liq yakunladi va barcha testlardan muvaffaqiyatli o'tkazdi.
Keyingi barcha agentlar (**3-agent: Qidiruv & Filtr**, **4-agent: Ijara & Bron**, **5-agent: AI Agent**, **6-agent: Frontend**) bevosita **sening yozgan modeling, repositorying, servising va API endpointlaringga** tayanadi.

---

## 📋 BOSQICH 0: LOYIHANI O'RGANISH (MAJBURIY, KODDAN OLDIN)

Kod yozishdan oldin quyidagi fayllar bilan to'liq tanishib chiq:

### O'qiladigan fayllar (tartibda):
1. `promptlar/1-agent-hisoboti.md` — 1-agent nimalar qilgani va hisoboti
2. `docs/ERKINOV_GOLIB_SHERZOD.md` — sening vazifalaring va qabul mezonlari
3. `backend/app/db/base.py` — `Base` class (SQLAlchemy DeclarativeBase)
4. `backend/app/db/session.py` — `AsyncSessionLocal`, `create_tables`
5. `backend/app/core/dependencies.py` — `get_db`, `get_current_user`, `get_current_admin`, `check_role`
6. `backend/app/core/exceptions.py` — `NotFoundError`, `ForbiddenError`, `BadRequestError`, `ConflictError`
7. `backend/app/schemas/common.py` — `PaginationParams`, `MessageResponse`
8. `backend/app/models/book.py` — hozirgi stub model (buni to'liq kengaytirasan)
9. `backend/app/api/v1/router.py` — v1 router (kitoblar routerini shu yerga ulaysan)
10. `backend/tests/test_auth.py` — test yozish uslubi va shabloni

---

## 🎯 SENING VAZIFANG

Sen Senior darajadagi **Clean / Layered Architecture** tamoyillari asosida quyidagi qatlamlarni to'liq amalga oshirasan:

| # | Qatlam | Fayllar | Maqsadi |
|---|---|---|---|
| 1 | **Model** | `backend/app/models/book.py` | `Book` SQLAlchemy 2.0 modeli (to'liq maydonlar bilan) |
| 2 | **Sxemalar** | `backend/app/schemas/book.py` | `BookCreate`, `BookUpdate`, `BookResponse`, `BookListResponse` |
| 3 | **Repository** | `backend/app/repositories/book_repo.py` | Data Access Layer (faqat SQL / DB amallari) |
| 4 | **Service** | `backend/app/services/book_service.py` | Business Logic Layer (mavjudlik tekshiruvi, biznes qoidalar) |
| 5 | **API Endpoints** | `backend/app/api/v1/books.py` | REST API (CRUD + ruxsatlar boshqaruvi) |
| 6 | **Router Integratsiyasi** | `backend/app/api/v1/router.py` | `/books` marshrutini ro'yxatdan o'tkazish |
| 7 | **Seed Data** | `backend/app/db/seed.py` | Boshlang'ich kitoblar to'plami (idempotent) |
| 8 | **Testlar** | `backend/tests/test_books.py` | Avtomatlashtirilgan Pytest testlari |

---

## 📐 BOSQICH 1: REJA TUZISH (KODDAN OLDIN YOZILADI)

### 1.1 Talablarni aniqlash
- **`Book` modeli:**
  - `id`: Integer (Primary Key, index=True)
  - `title`: String(255) (kitob nomi, index=True, nullable=False)
  - `author`: String(255) (muallif, index=True, nullable=False)
  - `genre`: String(100) (janr, index=True, nullable=False)
  - `year`: Integer (nashr yili, nullable=False)
  - `shelf_location`: String(100) (kutubxonadagi javon joylashuvi, masalan: "2-qavat, A-3 javon")
  - `status`: String(20) ("available" / "borrowed" / "reserved", default="available")
  - `description`: Text (ixtiyoriy tavsif, nullable=True)
  - `created_at`: DateTime(timezone=True)
  - `updated_at`: DateTime(timezone=True)

- **Ruxsatlar boshqaruvi (Permissions):**
  - `GET /api/v1/books` — Barcha uchun ochiq (mehmon, talaba, admin).
  - `GET /api/v1/books/{id}` — Barcha uchun ochiq.
  - `POST /api/v1/books` — Faqat **Admin** yoki **Librarian** (`check_role(["admin", "librarian"])`).
  - `PUT /api/v1/books/{id}` — Faqat **Admin** yoki **Librarian**.
  - `DELETE /api/v1/books/{id}` — Faqat **Admin** (`get_current_admin`).

- **Seed Data:**
  - Baza dastlab ishga tushganda kamida 8-10 ta haqiqiy va xilma-xil kitob (O'tkan kunlar, Mehrobdan chayon, Clean Code, Python Crash Course, Atomic Habits va h.k.) mavjud bo'lishi kerak.

### 1.2 Kelib chiqishi mumkin bo'lgan 7 ta muammo va ularning yechimlari:

```
MUAMMO 1: Kitob yangilanishida (PATCH/PUT) berilmagan maydonlarni None qilib yuborish
YECHIM 1: Pydantic v2 `model_dump(exclude_unset=True)` dan foydalanish,
          faqat so'rovda kelgan maydonlarnigina modelda yangilash.
```

```
MUAMMO 2: Kitob mavjud bo'lmaganda 500 yoki bo'sh javob qaytishi
YECHIM 2: Service qatlamida tekshirish va `backend.app.core.exceptions.NotFoundError`
          chaqirish (FastAPI avtomatik 404 JSON xatolik qaytaradi).
```

```
MUAMMO 3: 3-agent (Qidiruv) kitoblar ro'yxatini kengaytirganda repository buzilishi
YECHIM 3: Repository qatlamida `get_all` funksiyasini pagination (skip, limit) va
          kelgusida qidiruv filterlari ulanishiga mos toza SQLAlchemy `select()` bilan yozish.
```

```
MUAMMO 4: Ro'yxat qaytarishda jami kitoblar soni (total count) hisoblanmasligi
YECHIM 4: Pagination javobida `items` ro'yxati bilan birga `total`, `skip`, `limit`
          ko'rsatilgan `BookListResponse` sxemasidan foydalanish.
```

```
MUAMMO 5: Admin bo'lmagan foydalanuvchi kitob qo'shish/o'chirishga uringanda 500 berishi
YECHIM 5: 1-agent tomonidan tayyorlangan `check_role(["admin", "librarian"])` va
          `get_current_admin` dependency'laridan to'g'ri foydalanish (avtomatik 403 Forbidden qaytaradi).
```

```
MUAMMO 6: Kitob o'chirilganda bog'liq jadvallar (ijara/borrow) buzilishi
YECHIM 6: Hozircha kitob o'chirilishida xavfsiz soft-delete yoki statusni tekshirish,
          kelajakda 4-agent (Borrow) ulaganda cheklovlar qo'yilishi uchun struktura tayyorlash.
```

```
MUAMMO 7: Seed data har safar server o'chib yoqilganda qayta qo'shilib nusxalanishi
YECHIM 7: `seed_books()` funksiyasida avval kitoblar bor-yo'qligini tekshirish
          va faqat baza bo'sh bo'lgandagina ma'lumotlarni idempotent tarzda kiritish.
```

---

## 💻 BOSQICH 2: KOD YOZISH QOIDALARI VA SHABLONLAR

### 2.1 Model: `backend/app/models/book.py`
```python
# [Fayl maqsadi: Kitob (Book) SQLAlchemy modeli]
from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base

class BookStatus(str, PyEnum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    genre: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    shelf_location: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=BookStatus.AVAILABLE, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
```

### 2.2 Sxemalar: `backend/app/schemas/book.py`
- Pydantic v2 `ConfigDict(from_attributes=True)` bilan:
  - `BookBase`: `title`, `author`, `genre`, `year`, `shelf_location`, `status`, `description`
  - `BookCreate`: yangi kitob yaratish uchun (barcha majburiy maydonlar)
  - `BookUpdate`: kitobni tahrirlash uchun (barcha maydonlar ixtiyoriy: `Optional[...] = None`)
  - `BookResponse`: `id`, `created_at`, `updated_at` bilan birga to'liq ob'ekt
  - `BookListResponse`: `items: list[BookResponse]`, `total: int`, `skip: int`, `limit: int`

### 2.3 Repository: `backend/app/repositories/book_repo.py`
- `BookRepository` class:
  - `async def get_by_id(self, db: AsyncSession, book_id: int) -> Book | None`
  - `async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 20) -> tuple[list[Book], int]`
  - `async def create(self, db: AsyncSession, obj_in: BookCreate) -> Book`
  - `async def update(self, db: AsyncSession, db_obj: Book, update_data: dict[str, Any]) -> Book`
  - `async def delete(self, db: AsyncSession, db_obj: Book) -> None`

### 2.4 Service: `backend/app/services/book_service.py`
- `BookService` class:
  - Repository chaqiruvlari, xatoliklarni tekshirish:
  - Agar kitob topilmasa: `raise NotFoundError(detail="Kitob topilmadi")`
  - CRUD jarayonlarini to'liq boshqarish.

### 2.5 API Router: `backend/app/api/v1/books.py`
- `router = APIRouter()`
  - `GET /` -> `BookListResponse` (barcha uchun ochiq)
  - `GET /{book_id}` -> `BookResponse` (barcha uchun ochiq)
  - `POST /` -> `BookResponse` (Dependency: `check_role(["admin", "librarian"])`)
  - `PUT /{book_id}` -> `BookResponse` (Dependency: `check_role(["admin", "librarian"])`)
  - `DELETE /{book_id}` -> `MessageResponse` (Dependency: `get_current_admin`)

---

## ✅ BOSQICH 3: TEKSHIRISH VA TESTLAR

Ishni yakunlagach quyidagi tekshiruvlarni bajaring:

### 3.1 Avtomatlashtirilgan testlar: `backend/tests/test_books.py`
Kamida quyidagi 10 ta test yozilishi va `pytest` orqali muvaffaqiyatli o'tishi shart:
1. `test_get_books_empty_or_seeded` — kitoblar ro'yxatini olish
2. `test_get_book_by_id_success` — mavjud kitobni olish
3. `test_get_book_not_found` — mavjud bo'lmagan ID da 404 qaytishi
4. `test_create_book_as_admin_success` — admin kitob yarata olishi
5. `test_create_book_as_unauthorized_fails` — tokensiz so'rovda 401 qaytishi
6. `test_create_book_as_student_forbidden` — oddiy talaba kitob qo'shmoqchi bo'lsa 403 qaytishi
7. `test_update_book_success` — admin kitob ma'lumotlarini o'zgartirishi
8. `test_update_book_not_found` — mavjud bo'lmagan kitobni yangilashda 404
9. `test_delete_book_as_admin_success` — admin kitobni o'chira olishi
10. `test_delete_book_as_student_forbidden` — talaba kitobni o'chira olmasligi (403)

Testlarni ishga tushirish:
```bash
pytest backend/tests/test_books.py -v
```

---

## 📊 BOSQICH 4: HISOBOT (ISh TUGAGACH YOZILADI)

Ishni to'liq yakunlab, barcha testlar muvaffaqiyatli o'tgach, `promptlar/2-agent-hisoboti.md` fayliga quyidagi formatda hisobot yoz:

```markdown
# 🤖 2-AGENT: KITOBLAR DOMENI YAKUNIY HISOBOTI

## Yozilgan / Tahrirlangan fayllar:
| Fayl | Qator soni | Holat |
|---|---|---|
| backend/app/models/book.py | XX | ✅ |
| backend/app/schemas/book.py | XX | ✅ |
| backend/app/repositories/book_repo.py | XX | ✅ |
| backend/app/services/book_service.py | XX | ✅ |
| backend/app/api/v1/books.py | XX | ✅ |
| backend/app/api/v1/router.py | XX | ✅ |
| backend/app/db/seed.py | XX | ✅ |
| backend/tests/test_books.py | XX | ✅ |
| JAMI | ~XXX | |

## Test natijalari:
[pytest natijalaridan parcha]

## 📌 3-AGENT (Qidiruv & Filtr — Ollaberganov Sarvarbek) UCHUN ESLATMA:
- Book modeli: `backend.app.models.book.Book`
- BookRepository: `backend.app.repositories.book_repo.BookRepository`
- Sen `BookRepository`ga `search_and_filter()` metodini va qidiruv sxemalarini qo'shishing mumkin.
- API endpoint: `GET /api/v1/books` da `query`, `genre`, `author`, `year` parametrlari orqali filtrlashni kengaytirish uchun tayyor.
```

---

## ⚠️ MUHIM ESLATMALAR:
1. **Mavjud Auth tizimini buzmang:** 1-agent yaratgan `User`, `security.py`, `dependencies.py` fayllarini o'zgartirmang, faqat import qilib ishlating.
2. **Qatlamlarni aralashtirmang:** API faylida to'g'ridan-to'g'ri SQL yozmang. API faqat Service bilan, Service esa faqat Repository bilan gaplashadi.
3. **Hardcode qilmang:** Barcha xatoliklar va javoblar Pydantic sxemalari va maxsus Exceptionlar orqali qaytsin.