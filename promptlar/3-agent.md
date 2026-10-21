# 🤖 3-AGENT PROMPTI: QIDIRUV VA FILTRLASH DOMENI (SEARCH & FILTER)

Sen **ARM (Axborot Resurs Markazi)** loyihasining **uchinchi agenti** san (**Ollaberganov Sarvarbek — Backend Qidiruv & Filtr**).
1-agent loyihaning arxitekturaviy poydevori va autentifikatsiya tizimini, 2-agent esa kitoblar domeni (Books Core: model, sxemalar, repository, service va asosiy CRUD API) ni to'liq yakunladi va 26/26 ta testdan muvaffaqiyatli o'tkazdi.
Keyingi barcha agentlar (**4-agent: Ijara & Bron**, **5-agent: AI Agent**, **6-agent: Kiosk & Web Frontend**) bevosita **sening qidiruv va filtrlash endpointlaringga, kengaytirilgan repository metodlaringga va AI tavsiya bayroqlaringga** tayanadi.

---

## 📋 BOSQICH 0: LOYIHANI O'RGANISH (MAJBURIY, KODDAN OLDIN)

Kod yozishdan oldin quyidagi fayllar bilan to'liq tanishib chiq:

### O'qiladigan fayllar (tartibda):
1. `promptlar/2-agent-hisoboti.md` — 2-agent nimalar qilgani, yaratilgan modellar va eslatmalar
2. `docs/OLLABERGANOV_SARVARBEK_DAVRONBEK.md` — sening vazifalaring va qabul mezonlari
3. `backend/app/models/book.py` — `Book` modeli va `BookStatus` enum
4. `backend/app/schemas/book.py` — mavjud Pydantic sxemalari (`BookResponse`, `BookListResponse`)
5. `backend/app/repositories/book_repo.py` — `BookRepository` (buni qidiruv metodlari bilan kengaytirasan)
6. `backend/app/services/book_service.py` — `BookService` (qidiruv va AI tavsiyalar mantiqi)
7. `backend/app/api/v1/books.py` — kitoblar API routeri
8. `backend/tests/test_books.py` — 2-agent testlari (bular buzilmasligi shart)

---

## 🎯 SENING VAZIFANG

Sen Senior darajadagi **Clean / Layered Architecture** tamoyillari asosida quyidagi qatlamlarni kengaytirasan va to'liq amalga oshirasan:

| # | Qatlam | Fayllar | Maqsadi |
|---|---|---|---|
| 1 | **Sxemalar** | `backend/app/schemas/book.py` | `BookFilterParams` va `BookSearchResultResponse` sxemalari |
| 2 | **Repository** | `backend/app/repositories/book_repo.py` | `search_and_filter()` va `get_genres()` metodlari (SQLAlchemy ORM) |
| 3 | **Service** | `backend/app/services/book_service.py` | `search_books()` va bo'sh natijada `ask_ai: True` mantiqi |
| 4 | **API Endpoints** | `backend/app/api/v1/books.py` | `GET /api/v1/books/search` va `GET /api/v1/books/genres` endpointlari |
| 5 | **Sxemalar Eksporti** | `backend/app/schemas/__init__.py` | Yangi sxemalarni eksport qilish |
| 6 | **Testlar** | `backend/tests/test_search.py` | Qidiruv va filtr bo'yicha kamida 12 ta yangi Pytest testlari |

---

## 📐 BOSQICH 1: REJA VA TALABLAR TAHLILI

### 1.1 Talablarni aniqlash
- **Ko'p parametrli filtrlash imkoniyatlari:**
  - `query` (nom yoki muallif bo'yicha case-insensitive to'liq/qisman qidiruv)
  - `genre` (aniq yoki qisman janr filtri)
  - `author` (muallif bo'yicha filtr)
  - `status` ("available", "borrowed", "reserved")
  - `year_from` va `year_to` (nashr yillari oralig'i)
  - `sort_by` ("id", "title", "year", "created_at", default="id")
  - `order` ("asc", "desc", default="desc")
  - `skip` va `limit` (pagination)

- **AI Agent (5-agent) va Kiosk (6-agent) bilan integratsiya:**
  - Agar foydalanuvchi qidirgan kitob topilmasa (`total == 0` va `query` mavjud bo'lsa):
    - Javobda `ask_ai: true` qaytishi kerak.
    - `suggestions: list[str]` da foydalanuvchiga muqobil takliflar (masalan, mavjud o'xshash janrlar) qaytishi kerak.
    - HTTP status kodi: **200 OK** (qidiruv natijasi bo'sh bo'lganda 404 qaytarilmaydi, bo'sh ro'yxat va `ask_ai: true` qaytadi).

- **Mavjud tizimni saqlash (Backward Compatibility):**
  - 2-agent yozgan `GET /api/v1/books` endpointi va mavjud 26 ta test 100% buzilmasdan ishlashda davom etishi shart.

### 1.2 Kelib chiqishi mumkin bo'lgan 7 ta muammo va ularning yechimlari:

```
MUAMMO 1: SQLite va PostgreSQL o'rtasida Case-insensitive (katta-kichik harf) qidiruv farqi
YECHIM 1: `func.lower(Column).contains(func.lower(val))` usulidan foydalanish.
          Bu har ikki DBMS (SQLite va PostgreSQL) da bir xil xatoliksiz ishlaydi.
```

```
MUAMMO 2: Noma'lum `sort_by` maydoni orqali SQL Injection yoki AttributeError kelib chiqishi
YECHIM 2: Service/Repository qatlamida ruxsat etilgan maydonlar oq ro'yxatini (whitelist)
          joriy qilish: ALLOWED_SORT_FIELDS = {"id", "title", "year", "created_at"}.
          Noto'g'ri maydon kelsa, xato bermasdan xavfsiz `Book.id.desc()` ga fallback qilish.
```

```
MUAMMO 3: Qidiruv bo'yicha hech narsa topilmaganda 404 Not Found xatosi qaytarilishi
YECHIM 3: Qidiruvda topilmaslik xatolik emas, bu normal holat! Shuning uchun 200 OK kodi bilan
          `items: []`, `total: 0`, `ask_ai: True` va `suggestions` qaytarish.
```

```
MUAMMO 4: Qidiruv parametrlarida boshidagi/oxiridagi bo'sh joylar (spaces) tufayli natija topilmasligi
YECHIM 4: Pydantic validator yoki Python `strip()` orqali satrlarni tozalab olish
          (masalan: "  Alisher   " -> "Alisher").
```

```
MUAMMO 5: Ko'p filterlar qo'llanganda umumiy soni (total count) noto'g'ri hisoblanishi
YECHIM 5: Filtrlash shartlarini (`conditions`) alohida ro'yxatda yig'ish va bir xil `where(*conditions)`
          shartini ham `select(func.count())` ga, ham `select(Book)` ga qo'llash.
```

```
MUAMMO 6: Mavjud 2-agent yozgan testlarning buzilishi
YECHIM 6: Yangi endpointni `GET /api/v1/books/search` sifatida qo'shish va `GET /api/v1/books` ning
          mavjud signaturasini o'zgartirmasdan, qidiruv funksiyalarini alohida test faylida (`test_search.py`) sinash.
```

```
MUAMMO 7: Frontend uchun mavjud janrlar ro'yxatining dinamik emasligi
YECHIM 7: Maxsus `GET /api/v1/books/genres` endpointini yaratish va `select(distinct(Book.genre))`
          orqali bazadagi barcha unikal janrlar ro'yxatini qaytarish.
```

---

## 💻 BOSQICH 2: KOD YOZISH QOIDALARI VA SHABLONLAR

### 2.1 Sxemalar: `backend/app/schemas/book.py`
Fayl oxiriga quyidagi sxemalarni qo'shing:

```python
class BookFilterParams(BaseModel):
    query: str | None = Field(default=None, description="Kitob nomi yoki muallif bo'yicha qidiruv")
    genre: str | None = Field(default=None, description="Janr bo'yicha filtr")
    author: str | None = Field(default=None, description="Muallif ismi bo'yicha filtr")
    status: str | None = Field(default=None, description="Kitob holati: available, borrowed, reserved")
    year_from: int | None = Field(default=None, ge=0, le=2100, description="Nashr yilining quyi chegarasi")
    year_to: int | None = Field(default=None, ge=0, le=2100, description="Nashr yilining yuqori chegarasi")
    sort_by: str = Field(default="id", description="Saralash maydoni: id, title, year, created_at")
    order: str = Field(default="desc", description="Saralash tartibi: asc yoki desc")
    skip: int = Field(default=0, ge=0, description="O'tkazib yuboriladigan yozuvlar soni")
    limit: int = Field(default=20, ge=1, le=100, description="Qaytariladigan maksimal yozuvlar soni")


class BookSearchResultResponse(BaseModel):
    items: list[BookResponse]
    total: int
    skip: int
    limit: int
    ask_ai: bool = Field(default=False, description="Kitob topilmaganda AI Agentiga yo'naltirish bayrog'i")
    suggestions: list[str] = Field(default_factory=list, description="Foydalanuvchiga tavsiyalar ro'yxati")
```

### 2.2 Repository: `backend/app/repositories/book_repo.py`
`BookRepository` sinfiga quyidagi metodlarni qo'shing:

```python
    async def search_and_filter(
        self, db: AsyncSession, filters: BookFilterParams
    ) -> tuple[list[Book], int]:
        """Kitoblarni ko'p parametrli qidirish, filtrlash, saralash va sahifalash."""
        conditions = []

        if filters.query and filters.query.strip():
            q_clean = filters.query.strip().lower()
            conditions.append(
                or_(
                    func.lower(Book.title).contains(q_clean),
                    func.lower(Book.author).contains(q_clean),
                )
            )

        if filters.genre and filters.genre.strip():
            conditions.append(func.lower(Book.genre).contains(filters.genre.strip().lower()))

        if filters.author and filters.author.strip():
            conditions.append(func.lower(Book.author).contains(filters.author.strip().lower()))

        if filters.status and filters.status.strip():
            conditions.append(Book.status == filters.status.strip().lower())

        if filters.year_from is not None:
            conditions.append(Book.year >= filters.year_from)

        if filters.year_to is not None:
            conditions.append(Book.year <= filters.year_to)

        # 1. Total count
        count_stmt = select(func.count()).select_from(Book)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_res = await db.execute(count_stmt)
        total = count_res.scalar() or 0

        # 2. Saralash (Sorting whitelist)
        allowed_sorts = {
            "id": Book.id,
            "title": Book.title,
            "year": Book.year,
            "created_at": Book.created_at,
        }
        sort_col = allowed_sorts.get(filters.sort_by.lower(), Book.id)
        order_by = sort_col.asc() if filters.order.lower() == "asc" else sort_col.desc()

        # 3. Natijalarni olish
        query_stmt = select(Book)
        if conditions:
            query_stmt = query_stmt.where(and_(*conditions))
        query_stmt = query_stmt.order_by(order_by).offset(filters.skip).limit(filters.limit)

        result = await db.execute(query_stmt)
        books = list(result.scalars().all())

        return books, total

    async def get_all_genres(self, db: AsyncSession) -> list[str]:
        """Bazadagi mavjud barcha unikal janrlar ro'yxatini qaytarish."""
        stmt = select(Book.genre).distinct().order_by(Book.genre.asc())
        result = await db.execute(stmt)
        return [row[0] for row in result.all() if row[0]]
```

### 2.3 Service: `backend/app/services/book_service.py`
`BookService` sinfiga qidiruv biznes mantig'ini qo'shing:

```python
    async def search_books(
        self, db: AsyncSession, filters: BookFilterParams
    ) -> BookSearchResultResponse:
        """Kitoblarni qidirish va natijalarni AI tavsiyalari bilan boyitish."""
        items, total = await self.repo.search_and_filter(db, filters)
        ask_ai = False
        suggestions = []

        # Agar qidiruv bo'yicha hech narsa topilmasa va qidiruv so'rovi bo'lsa:
        if total == 0 and (filters.query or filters.genre or filters.author):
            ask_ai = True
            all_genres = await self.repo.get_all_genres(db)
            suggestions = [f"Mavjud janr: {g}" for g in all_genres[:4]]

        return BookSearchResultResponse(
            items=items,
            total=total,
            skip=filters.skip,
            limit=filters.limit,
            ask_ai=ask_ai,
            suggestions=suggestions,
        )

    async def get_genres(self, db: AsyncSession) -> list[str]:
        """Mavjud barcha janrlarni olish."""
        return await self.repo.get_all_genres(db)
```

### 2.4 API Router: `backend/app/api/v1/books.py`
Routerga ikkita yangi ochiq endpoint qo'shing:

```python
@router.get(
    "/search",
    response_model=BookSearchResultResponse,
    summary="Kitoblarni qidirish va filtrlash",
    description="Nom, muallif, janr, holat va nashr yili bo'yicha qidiruv. Bo'sh natijada AI tavsiya beradi.",
)
async def search_books(
    db: Annotated[AsyncSession, Depends(get_db)],
    filters: Annotated[BookFilterParams, Depends()],
) -> BookSearchResultResponse:
    """Kitoblarni ko'p parametrli qidirish va filtrlash."""
    return await book_service.search_books(db, filters)


@router.get(
    "/genres",
    response_model=list[str],
    summary="Barcha mavjud janrlar ro'yxatini olish",
    description="Kutubxonadagi mavjud unikal janrlar ro'yxatini qaytaradi (Frontend filtrlari uchun).",
)
async def get_genres(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[str]:
    """Mavjud janrlar ro'yxatini qaytarish."""
    return await book_service.get_genres(db)
```

---

## ✅ BOSQICH 3: TEKSHIRISH VA TESTLAR

Ishni yakunlagach quyidagi testlarni amalga oshiring:

### 3.1 Avtomatlashtirilgan testlar: `backend/tests/test_search.py`
Kamida quyidagi 12 ta test yozilishi va muvaffaqiyatli o'tishi shart:
1. `test_search_by_title_partial` — kitob nomining qismi bo'yicha qidirish ("kunlar" -> "O'tkan kunlar")
2. `test_search_case_insensitive` — katta va kichik harflarda bir xil topilishi ("clean code" va "CLEAN CODE")
3. `test_search_by_author` — muallif ismi bo'yicha qidirish ("Qodiriy")
4. `test_filter_by_genre` — janr bo'yicha filtrlash ("Dasturlash")
5. `test_filter_by_year_range` — yil oralig'i bo'yicha filtrlash (`year_from=2015`, `year_to=2020`)
6. `test_filter_by_status` — holat bo'yicha filtrlash (`status="available"`)
7. `test_combined_search_and_filter` — bir vaqtda bir nechta parametr bilan filtrlash (query + genre + year_from)
8. `test_search_sorting_asc_desc` — `sort_by="year"` va `order="asc"` hamda `"desc"` bo'yicha saralash
9. `test_search_invalid_sort_fallback` — noto'g'ri `sort_by="not_real_column"` kiritilganda xato bermay ishlashi
10. `test_search_pagination` — qidiruv natijalarini `skip` va `limit` bilan sahifalash
11. `test_search_no_results_triggers_ask_ai` — topilmagan so'rovda `ask_ai: True` va `suggestions` qaytishi
12. `test_get_genres_endpoint` — `GET /api/v1/books/genres` unikal janrlar ro'yxatini to'g'ri qaytarishi

Testlarni ishga tushirish:
```bash
pytest backend/tests/test_search.py -v
pytest -v
```
(Barcha mavjud auth, books va yangi search testlari — kamida 38 ta test 100% muvaffaqiyatli o'tishi kerak!)

---

## 📊 BOSQICH 4: HISOBOT (ISh TUGAGACH YOZILADI)

Barcha ishlar tugagach va testlar to'liq o'tgach, `promptlar/3-agent-hisoboti.md` fayliga quyidagi formatda hisobot yoz:

```markdown
# 🤖 3-AGENT: QIDIRUV VA FILTRLASH DOMENI YAKUNIY HISOBOTI

## Yozilgan / Tahrirlangan fayllar:
| Fayl | Qator soni | Holat |
|---|---|---|
| backend/app/schemas/book.py | XX | ✅ |
| backend/app/schemas/__init__.py | XX | ✅ |
| backend/app/repositories/book_repo.py | XX | ✅ |
| backend/app/services/book_service.py | XX | ✅ |
| backend/app/api/v1/books.py | XX | ✅ |
| backend/tests/test_search.py | XX | ✅ |
| JAMI | ~XXX | ✅ |

## Test natijalari:
[pytest natijalaridan parcha]

## 📌 4-AGENT (Ijara & Bron — Shahriddinov Navro'zbek) VA 5-AGENT (AI Agent) UCHUN ESLATMA:
- Qidiruv endpointi: `GET /api/v1/books/search`
- Janrlar ro'yxati: `GET /api/v1/books/genres`
- Qidiruv natijasida kitob topilmasa `ask_ai: true` va `suggestions` qaytadi, 5-agent AI bilan bog'lash uchun to'liq tayyor.
- 4-agent kitob ijaraga olinganda statusini o'zgartirsa, qidiruv avtomatik tarzda `status="available"` orqali faqat bo'sh kitoblarni ko'rsatadi.
```

---

## 🌿 Ishchi Branch
`sarvarbek/search`

## ⚠️ MUHIM ESLATMALAR:
1. **Mavjud Auth va Books Core tizimini buzmang:** 1-agent va 2-agent yozgan testlar va endpointlar o'zgarmasdan ishlashi shart.
2. **SQL Injection xavfidan saqlaning:** Barcha qidiruvlar SQLAlchemy parametrlari va oq ro'yxat (whitelist) orqali amalga oshirilsin.
3. **HTTP 200 vs 404:** Qidiruvda natija topilmasligi xato emas — 200 OK kodi bilan bo'sh ro'yxat va AI taklifi qaytsin.
