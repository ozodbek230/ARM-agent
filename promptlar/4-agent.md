# 🤖 4-AGENT PROMPTI: IJARA VA BRON DOMENI (BORROW & RESERVATION CORE)

Sen **ARM (Axborot Resurs Markazi)** loyihasining **to'rtinchi agenti** san (**Shahriddinov Navro'zbek — Backend Ijara & Bron Domeni**).
Oldingi barcha agentlar o'z vazifalarini 100% bajardilar:
- **1-agent:** Arxitektura poydevori, ma'lumotlar bazasi, User modeli va JWT autentifikatsiya.
- **2-agent:** Kitoblar domeni (Books Core: model, sxemalar, repository, service, REST CRUD API, seed data).
- **3-agent:** Qidiruv va ko'p parametrli filtrlash tizimi (Search & Filter, AI tavsiya bayrog'i, unikal janrlar).
- Hozirda tizimda jami **38 ta avtomatlashtirilgan test** mavjud va barchasi muvaffaqiyatli o'tgan (**38/38 PASSED**).

Keyingi barcha agentlar (**5-agent: AI Agent**, **6-agent: Kiosk & Web Frontend**) bevosita **sening kitob olish (Borrow), qaytarish (Return), navbatga yozilish (Reservation) va muddatlarni tekshirish API'laringga** tayanadi.

---

## 📋 BOSQICH 0: LOYIHANI O'RGANISH (MAJBURIY, KODDAN OLDIN)

Kod yozishdan oldin quyidagi fayllar bilan to'liq tanishib chiq:

### O'qiladigan fayllar (tartibda):
1. `promptlar/3-agent-hisoboti.md` — 3-agent nimalar qilgani va hisoboti
2. `docs/SHAHRIDDINOV_NAVROZBEK_OTKIRBEK.md` — sening vazifalaring va qabul mezonlari
3. `backend/app/models/user.py` — `User` modeli va rollar (`admin`, `user`, `librarian`)
4. `backend/app/models/book.py` — `Book` modeli va `BookStatus` ("available", "borrowed", "reserved")
5. `backend/app/models/borrow.py` — hozirgi stub model (`Borrow` va `Reservation` ni shu yerda kengaytirasan)
6. `backend/app/core/dependencies.py` — `get_db`, `get_current_user`, `get_current_admin`, `check_role`
7. `backend/app/core/exceptions.py` — `NotFoundError`, `BadRequestError`, `ForbiddenError`, `ConflictError`
8. `backend/app/api/v1/router.py` — v1 router (`borrows_router` ni shu yerga ulaysan)
9. `backend/tests/test_books.py` va `backend/tests/test_search.py` — test yozish uslubi va shabloni

---

## 🎯 SENING VAZIFANG

Sen Senior darajadagi **Clean / Layered Architecture** tamoyillari asosida quyidagi qatlamlarni to'liq amalga oshirasan:

| # | Qatlam | Fayllar | Maqsadi |
|---|---|---|---|
| 1 | **Modellar** | `backend/app/models/borrow.py` | `Borrow` va `Reservation` SQLAlchemy 2.0 modellari |
| 2 | **Modellar Eksporti** | `backend/app/models/__init__.py` | `Borrow`, `Reservation`, `BorrowStatus`, `ReservationStatus` ni eksport qilish |
| 3 | **Sxemalar** | `backend/app/schemas/borrow.py` | `BorrowCreate`, `BorrowResponse`, `ReturnRequest`, `ReservationCreate`, `ReservationResponse`, `BorrowListResponse` |
| 4 | **Sxemalar Eksporti** | `backend/app/schemas/__init__.py` | Yangi sxemalarni markaziy eksportga kiritish |
| 5 | **Repository** | `backend/app/repositories/borrow_repo.py` | DB operatsiyalari (ijara yaratish, qaytarish, bron qilish, navbat o'rinlarini boshqarish) |
| 6 | **Service** | `backend/app/services/borrow_service.py` | Biznes mantiq (14 kunlik muddat, 3 kishilik navbat chegarasi, kitob holatini o'zgartirish, overdue tekshiruvi) |
| 7 | **API Endpoints** | `backend/app/api/v1/borrows.py` | REST API (kitob olish, qaytarish, mening kitoblarim, bron qilish, bronni bekor qilish, overdue) |
| 8 | **Router Integratsiyasi** | `backend/app/api/v1/router.py` | `/borrows` marshrutini ro'yxatdan o'tkazish |
| 9 | **Testlar** | `backend/tests/test_borrows.py` | Kamida 14 ta avtomatlashtirilgan Pytest testlari |

---

## 📐 BOSQICH 1: REJA VA BIZNES TALABLAR TAHLILI

### 1.1 Talablar va Mantiqiy Qoidalar:
1. **Kitob olish (Borrow):**
   - Faqat tizimga kirgan (avtorizatsiyadan o'tgan) foydalanuvchi kitob ola oladi (`get_current_user`).
   - Kitob holati faqat **"available"** bo'lsagina ijaraga beriladi.
   - Kitob berilgach:
     - `Borrow` yozuvi yaratiladi: `borrow_date = now`, `due_date = now + 14 kun`, `status = "active"`.
     - `Book.status` darhol **"borrowed"** ga o'zgaradi.
   - Agar kitob holati `"borrowed"` yoki `"reserved"` bo'lsa:
     - To'g'ridan-to'g'ri ijara berilmaydi, `BadRequestError(detail="Kitob hozirda band. Faqat bron (navbat) qilishingiz mumkin.")` qaytariladi.

2. **Kitob qaytarish (Return):**
   - Kitob qaytarilganda (`borrow_id` yoki `book_id` orqali):
     - `Borrow.returned_date = now` qilinadi va `Borrow.status = "returned"` ga o'tkaziladi.
     - **Navbatni tekshirish mantiqi:**
       - Agar ushbu kitob uchun kutayotgan bronlar mavjud bo'lsa (`Reservation.status == "waiting"` va `queue_position == 1`):
         - 1-o'rindagi bron statusi **"notified"** ga o'tadi (foydalanuvchiga xabar berish uchun).
         - Kitob statusi **"reserved"** bo'ladi (boshqa birov olib ketmasligi uchun saqlanadi).
       - Agar kitob uchun hech qanday kutayotgan navbat bo'lmasa:
         - `Book.status` yana **"available"** holatiga qaytariladi.

3. **Bron qilish / Navbatga yozilish (Reservation):**
   - Bron qilish **faqat hozirda band bo'lgan** (`status in ["borrowed", "reserved"]`) kitoblar uchun ruxsat etiladi.
   - Agar kitob bo'sh ("available") bo'lsa, uni bron qilishga urinishda:
     - `BadRequestError(detail="Kitob hozirda bo'sh, uni to'g'ridan-to'g'ri ijaraga olishingiz mumkin.")` qaytariladi.
   - **Bitta kitobga bitta foydalanuvchi faqat 1 marta navbatga yozilishi mumkin:**
     - Agar foydalanuvchi allaqachon ushbu kitob navbatida turgan bo'lsa (`status in ["waiting", "notified"]`):
       - `BadRequestError(detail="Siz allaqachon ushbu kitob uchun navbatga yozilgansiz.")` qaytariladi.
   - **Maksimal 3 kishilik navbat chegarasi:**
     - Har bir kitob uchun ayni paytda eng ko'pi bilan 3 ta aktiv bron bo'lishi mumkin.
     - Agar navbatda allaqachon 3 kishi bo'lsa va 4-odam navbatga yozilmoqchi bo'lsa:
       - `BadRequestError(detail="Ushbu kitob uchun navbat to'lgan (maksimal 3 kishi).")` qaytariladi.
     - Navbat o'rni (`queue_position`) avtomatik ravishda mavjud kutayotganlar soniga qarab `1`, `2` yoki `3` qilib belgilanadi.

4. **Bronni bekor qilish (Cancel Reservation):**
   - Foydalanuvchi o'zi yaratgan bronni bekor qilishi mumkin (`status = "cancelled"`). Admin yoki Librarian ham bekor qila oladi.
   - Bron bekor qilinganda:
     - Orqadagi barcha navbatdagilarning o'rni 1 qadam oldinga siljiydi (masalan, 2-o'rindagi 1-o'ringa, 3-o'rindagi 2-o'ringa o'tadi).
     - Agar bekor qilingan bron "notified" holatda bo'lgan bo'lsa:
       - Navbatda keyingi odam bo'lsa, u "notified" qilinadi.
       - Navbatda hech kim qolmagan bo'lsa, kitob holati "available" ga qaytariladi.

5. **Mening kitoblarim (`GET /api/v1/borrows/my`):**
   - Joriy foydalanuvchining faol va qaytarilgan ijaralari ro'yxati kitob tafsilotlari (`book` ob'ekti) bilan birga qaytadi.

6. **Muddati o'tgan kitoblar (`GET /api/v1/borrows/overdue`):**
   - `due_date < now` bo'lgan va hali qaytarilmagan (`returned_date is None`) barcha ijara yozuvlarini qaytarish (Admin va Librarian ko'rishi mumkin).

---

### 1.2 Kelib chiqishi mumkin bo'lgan 7 ta muammo va ularning yechimlari:

```
MUAMMO 1: Vaqt zonalari (timezone aware vs naive) chalkashligi tufayli SQLite xatolik berishi
YECHIM 1: Barcha vaqtlarni standart `datetime.now(timezone.utc)` bilan generatsiya qilish,
          muddatni esa aniq `timedelta(days=14)` orqali hisoblash.
```

```
MUAMMO 2: Kitob qaytarilganda navbatdagi odamlar o'rni (queue_position) buzilib ketishi
YECHIM 2: Repository qatlamida bron bekor qilinganda yoki yakunlanganda:
          `UPDATE reservations SET queue_position = queue_position - 1 WHERE book_id = :id AND queue_position > :cancelled_pos AND status = 'waiting'`
          mantiqini qat'iy yozish.
```

```
MUAMMO 3: Foydalanuvchi boshqa birovning ijarasini qaytarishga yoki boshqaning bronini o'chirishga urinishi
YECHIM 3: Service qatlamida tekshirish: agar `borrow.user_id != current_user.id` bo'lsa va
          foydalanuvchi admin/kutubxonachi bo'lmasa, `ForbiddenError` (403) qaytarish.
```

```
MUAMMO 4: Kitob allaqachon qaytarilgan bo'lsa ham qayta "qaytarish" so'rovi yuborilishi
YECHIM 4: Agar `borrow.status == "returned"` bo'lsa, `BadRequestError(detail="Ushbu kitob allaqachon qaytarilgan")`
          tashlash.
```

```
MUAMMO 5: 4-odam navbatga yozilayotganda chegaraning tekshirilmasligi
YECHIM 5: Bron yaratishdan oldin `SELECT COUNT(*) FROM reservations WHERE book_id = :id AND status IN ('waiting', 'notified')`
          tekshirib, agar count >= 3 bo'lsa, `BadRequestError` tashlash.
```

```
MUAMMO 6: Bo'sh kitobga bron ochilishiga yo'l qo'yilishi
YECHIM 6: Bron yaratishda kitob holatini tekshirish: agar `book.status == "available"` bo'lsa,
          foydalanuvchini to'g'ridan-to'g'ri ijaraga olishga undovchi `BadRequestError` qaytarish.
```

```
MUAMMO 7: Mavjud 38 ta test (auth, books, search) buzilishi
YECHIM 7: Borrow moduli to'liq alohida qatlamda bo'ladi, mavjud modellar (`User`, `Book`) o'zgartirilmaydi,
          faqat `Book.status` xizmat amallari davomida yangilanadi.
```

---

## 💻 BOSQICH 2: KOD YOZISH QOIDALARI VA SHABLONLAR

### 2.1 Modellar: `backend/app/models/borrow.py`
Faylni quyidagi to'liq kod bilan yozing:

```python
# [Fayl maqsadi: Ijara (Borrow) va Bron (Reservation) SQLAlchemy modellari]
from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class BorrowStatus(str, PyEnum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class ReservationStatus(str, PyEnum):
    WAITING = "waiting"
    NOTIFIED = "notified"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    borrow_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    returned_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=BorrowStatus.ACTIVE.value,
        nullable=False,
    )

    # Aloqalar (Relationships)
    user = relationship("User", backref="borrows", lazy="selectin")
    book = relationship("Book", backref="borrows", lazy="selectin")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    reserved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    queue_position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=ReservationStatus.WAITING.value,
        nullable=False,
    )

    user = relationship("User", backref="reservations", lazy="selectin")
    book = relationship("Book", backref="reservations", lazy="selectin")
```

`backend/app/models/__init__.py` da `Borrow, Reservation, BorrowStatus, ReservationStatus` ni eksport qilishni unutmang.

---

### 2.2 Sxemalar: `backend/app/schemas/borrow.py`
Pydantic v2 sxemalari:

```python
# [Fayl maqsadi: Ijara va bron uchun Pydantic v2 sxemalari]
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.book import BookResponse
from backend.app.schemas.user import UserResponse


class BorrowCreate(BaseModel):
    book_id: int = Field(..., description="Ijaraga olinayotgan kitob identifikatori")
    days: int = Field(default=14, ge=1, le=30, description="Ijara muddati (kunlar soni, sukut bo'yicha 14 kun)")


class ReturnRequest(BaseModel):
    book_id: int | None = Field(default=None, description="Qaytarilayotgan kitob ID si")
    borrow_id: int | None = Field(default=None, description="Ijara yozuvi ID si")


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    returned_date: datetime | None = None
    status: str
    book: BookResponse | None = None
    user: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class BorrowListResponse(BaseModel):
    items: list[BorrowResponse]
    total: int


class ReservationCreate(BaseModel):
    book_id: int = Field(..., description="Bron qilinayotgan kitob identifikatori")


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    reserved_at: datetime
    queue_position: int
    status: str
    book: BookResponse | None = None
    user: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class ReservationListResponse(BaseModel):
    items: list[ReservationResponse]
    total: int
```

`backend/app/schemas/__init__.py` da barcha yangi sxemalarni eksport qiling.

---

### 2.3 Repository: `backend/app/repositories/borrow_repo.py`
`BorrowRepository` sinfi ma'lumotlar bazasi bilan toza async amallarni bajaradi:
- `get_borrow_by_id(db, borrow_id) -> Borrow | None`
- `get_active_borrow_by_book(db, book_id) -> Borrow | None`
- `get_user_borrows(db, user_id, active_only=False) -> list[Borrow]`
- `get_overdue_borrows(db) -> list[Borrow]`
- `create_borrow(db, user_id, book_id, days=14) -> Borrow`
- `mark_as_returned(db, borrow: Borrow) -> Borrow`
- `get_book_reservations(db, book_id, active_only=True) -> list[Reservation]`
- `get_user_reservation_for_book(db, user_id, book_id) -> Reservation | None`
- `get_user_reservations(db, user_id) -> list[Reservation]`
- `get_reservation_by_id(db, reservation_id) -> Reservation | None`
- `create_reservation(db, user_id, book_id, queue_position) -> Reservation`
- `cancel_reservation(db, reservation: Reservation) -> None`
- `shift_queue_positions(db, book_id, from_position: int) -> None` (orqadagi navbatdagilarni 1 qadam oldinga siljitish)

---

### 2.4 Service: `backend/app/services/borrow_service.py`
`BorrowService` sinfi barcha biznes mantiqlarni boshqaradi:
- `borrow_book(db, user_id, borrow_in: BorrowCreate) -> BorrowResponse`:
  - Kitob mavjudligini tekshirish (`book_repo.get_by_id`), topilmasa `NotFoundError("Kitob topilmadi")`.
  - Kitob holatini tekshirish: agar `book.status != "available"`, `BadRequestError("Kitob hozirda band. Faqat bron (navbat) qilishingiz mumkin.")`.
  - `Borrow` yaratish va `book.status = "borrowed"` qilib yangilash.
- `return_book(db, current_user, return_in: ReturnRequest) -> BorrowResponse`:
  - Ijara yozuvini aniqlash (`borrow_id` yoki `book_id` orqali).
  - Agar topilmasa yoki allaqachon qaytarilgan bo'lsa mos xatolik (`NotFoundError` yoki `BadRequestError`).
  - Agar oddiy foydalanuvchi bo'lsa va `borrow.user_id != current_user.id` bo'lsa, `ForbiddenError("Faqat o'zingiz olgan kitobni qaytarishingiz mumkin")` (Admin/Librarian har qanday kitobni qaytara oladi).
  - Ijarani qaytarish (`returned_date = now`, `status = "returned"`).
  - Navbatni tekshirish:
    - Agar kitob uchun kutayotgan bronlar bo'lsa: 1-o'rindagi bronni `status = "notified"` qilish va `book.status = "reserved"` qilish.
    - Agar kutayotgan bronlar bo'lmasa: `book.status = "available"` qilish.
- `reserve_book(db, user_id, reserve_in: ReservationCreate) -> ReservationResponse`:
  - Kitob mavjudligini tekshirish.
  - Agar kitob holati `"available"` bo'lsa: `BadRequestError("Kitob hozirda bo'sh, uni to'g'ridan-to'g'ri ijaraga olishingiz mumkin.")`.
  - Foydalanuvchi allaqachon shu kitob navbatidami: agar ha bo'lsa `BadRequestError("Siz allaqachon ushbu kitob uchun navbatga yozilgansiz.")`.
  - Faol navbatdagilar sonini tekshirish: agar `len(active_reservations) >= 3`, `BadRequestError("Ushbu kitob uchun navbat to'lgan (maksimal 3 kishi).")`.
  - Yangi o'rinni hisoblash: `queue_position = len(active_reservations) + 1`.
  - Bron yaratish.
- `cancel_reservation(db, current_user, reservation_id: int) -> MessageResponse`:
  - Bron mavjudligini tekshirish.
  - Huquqni tekshirish (o'zining broni yoki admin/librarian).
  - Bronni bekor qilish va qolgan navbatdagilarni siljitish.
  - Agar navbat bo'shab qolsa va kitob reserved bo'lgan bo'lsa, kitobni `available` qilish.
- `get_my_borrows(db, user_id) -> BorrowListResponse`
- `get_my_reservations(db, user_id) -> ReservationListResponse`
- `get_overdue_borrows(db) -> BorrowListResponse`

---

### 2.5 API Router: `backend/app/api/v1/borrows.py`
REST endpointlari:
- `POST /api/v1/borrows` — Yangi kitob olish (Auth talab qilinadi, 201 Created)
- `POST /api/v1/borrows/return` — Kitob qaytarish (Auth talab qilinadi, 200 OK)
- `GET /api/v1/borrows/my` — Mening kitoblarim (Auth talab qilinadi, 200 OK)
- `GET /api/v1/borrows/overdue` — Muddati o'tgan kitoblar ro'yxati (Faqat Admin yoki Librarian, 200 OK)
- `POST /api/v1/borrows/reservations` — Kitobga navbatga yozilish (Auth talab qilinadi, 201 Created)
- `GET /api/v1/borrows/reservations/my` — Mening bronlarim (Auth talab qilinadi, 200 OK)
- `DELETE /api/v1/borrows/reservations/{reservation_id}` — Bronni bekor qilish (Auth talab qilinadi, 200 OK)

### 2.6 Router Integratsiyasi: `backend/app/api/v1/router.py`
```python
from backend.app.api.v1.borrows import router as borrows_router
api_router.include_router(borrows_router, prefix="/borrows", tags=["Borrows & Reservations"])
```

---

## ✅ BOSQICH 3: TEKSHIRISH VA TESTLAR

Ishni yakunlagach `backend/tests/test_borrows.py` faylida kamida quyidagi **14 ta test** yozilishi va `pytest` orqali muvaffaqiyatli o'tishi shart:

1. `test_borrow_available_book_success` — bo'sh kitobni ijaraga olish va kitob statusi "borrowed" ga aylanishi
2. `test_borrow_already_borrowed_book_fails` — band kitobni olishga urinishda 400 xatolik chiqishi
3. `test_borrow_nonexistent_book_fails` — mavjud bo'lmagan kitobda 404 chiqishi
4. `test_borrow_unauthorized_fails` — tokensiz so'rovda 401 chiqishi
5. `test_return_book_success` — kitob qaytarilganda uning holati "available" ga aylanishi
6. `test_return_already_returned_book_fails` — qaytarilgan kitobni qayta qaytarishda 400 chiqishi
7. `test_return_other_users_book_forbidden` — boshqa birovning kitobini qaytarishga urinishda 403 chiqishi (admin bundan mustasno)
8. `test_get_my_borrows` — foydalanuvchi faqat o'ziga tegishli kitoblarni ko'rishi
9. `test_reserve_borrowed_book_success` — band kitobga navbatga yozilish (queue_position = 1)
10. `test_reserve_available_book_fails` — bo'sh turgan kitobni bron qilishga urinishda 400 chiqishi
11. `test_duplicate_reservation_fails` — bir kitobga ayni foydalanuvchi qayta navbatga yozila olmasligi
12. `test_reservation_queue_max_limit` — 4-odam navbatga yozilmoqchi bo'lsa navbat to'lgan deb 400 qaytishi
13. `test_return_book_notifies_first_in_queue` — kitob qaytarilganda 1-o'rindagi bron "notified" va kitob "reserved" bo'lishi
14. `test_cancel_reservation_shifts_queue` — bron bekor qilinganda qolganlarning o'rni oldinga siljishi

### Testlarni ishga tushirish:
```bash
pytest backend/tests/test_borrows.py -v
pytest -v
```
(Barcha testlar: 14 auth + 12 books + 12 search + 14 borrows = **kamida 52 ta test 100% muvaffaqiyatli o'tishi shart!**)

---

## 📊 BOSQICH 4: HISOBOT (ISh TUGAGACH YOZILADI)

Barcha testlar muvaffaqiyatli o'tgach, `promptlar/4-agent-hisoboti.md` fayliga quyidagi formatda hisobot yoz:

```markdown
# 🤖 4-AGENT: IJARA VA BRON DOMENI YAKUNIY HISOBOTI

## Yozilgan / Tahrirlangan fayllar:
| Fayl | Qator soni | Holat |
|---|---|---|
| backend/app/models/borrow.py | XX | ✅ |
| backend/app/models/__init__.py | XX | ✅ |
| backend/app/schemas/borrow.py | XX | ✅ |
| backend/app/schemas/__init__.py | XX | ✅ |
| backend/app/repositories/borrow_repo.py | XX | ✅ |
| backend/app/services/borrow_service.py | XX | ✅ |
| backend/app/api/v1/borrows.py | XX | ✅ |
| backend/app/api/v1/router.py | XX | ✅ |
| backend/tests/test_borrows.py | XX | ✅ |
| JAMI | ~XXX | ✅ |

## Test natijalari:
[pytest natijalaridan parcha]

## 📌 5-AGENT (AI Agent — Rahimboyev A'zamjon) VA 6-AGENT (Frontend) UCHUN ESLATMA:
- Kitob olish endpointi: `POST /api/v1/borrows`
- Qaytarish endpointi: `POST /api/v1/borrows/return`
- Mening kitoblarim: `GET /api/v1/borrows/my`
- Navbatga yozilish: `POST /api/v1/borrows/reservations`
- Navbat chegarasi: har bir kitob uchun maksimal 3 ta odam.
- 5-agent (AI): foydalanuvchiga kitob tavsiya qilganda uning `status` ini tekshirib, agar "borrowed" bo'lsa navbatga yozilishni taklif qilishi mumkin.
```

---

## 🌿 Ishchi Branch
`navrozbek/booking`

## ⚠️ MUHIM ESLATMALAR:
1. **Mavjud Auth, Books Core va Search tizimlarini buzmang:** Oldingi 3 ta agent yaratgan 38 ta test 100% o'tishda davom etishi shart.
2. **Qatlamlarni aralashtirmang:** API faqat Service bilan, Service esa faqat Repository bilan gaplashadi.
3. **Tranzaksion butunlik:** Kitob holati va ijara/bron yozuvlari birgalikda to'g'ri commit qilinishi kerak.
