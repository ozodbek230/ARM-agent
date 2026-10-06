# OLLABERGANOV SARVARBEK DAVRONBEK O'G'LI — Backend (Qidiruv & Filtr)

**Rol:** Kitoblar katalogini tezkor qidirish, ko'p parametrli filtrlash va saralash mantiqi bo'yicha mas'ul muhandis.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **Qidiruv sxemalari (`backend/app/schemas/book.py` ga qo'shimcha):**
  - `BookFilterParams` — Pydantic modeli:
    - `query`: Optional[str] (nom va muallif bo'yicha erkin qidiruv)
    - `genre`: Optional[str] (janr bo'yicha filtr)
    - `author`: Optional[str] (muallif bo'yicha filtr)
    - `status`: Optional[str] (faqat "available" / bo'sh kitoblarni ko'rish)
    - `year_from`, `year_to`: Optional[int]
    - `sort_by`: Optional[str] ("title", "year", "created_at")
    - `order`: Optional[str] ("asc", "desc")
- [ ] **Repository Qidiruv Metodlari (`backend/app/repositories/book_repo.py` ga qo'shimcha):**
  - `search_and_filter(db: AsyncSession, filters: BookFilterParams, skip: int = 0, limit: int = 20) -> Tuple[List[Book], int]`
  - Qidiruvda `ILIKE` yoki `LOWER()` ishlatish (katta-kichik harf sezgir bo'lmasligi uchun).
  - So'rov parametrlarini xavfsiz tarzda SQL injectionlarsiz SQLAlchemy ORM orqali yig'ish.
- [ ] **Xizmat qatlami (`backend/app/services/book_service.py` ga qo'shimcha):**
  - Qidiruv natijalarini boyitish: agar qidiruv bo'sh qaytsa, `{"suggestions": ["O'xshash janrlar..."], "ask_ai": True}` bayrog'ini qaytarish.
- [ ] **API Endpointi (`backend/app/api/v1/books.py` ga integratsiya):**
  - `GET /api/v1/books/search` (yoki `/api/v1/books` ning query parametrlari orqali):
    - `q`, `genre`, `status`, `page`, `page_size`
- [ ] **Tezlik va optimallashtirish:**
  - Qidiruv so'rovi 200ms dan oshmasligi kerak.

---

## 🔗 Jamoaga Bog'liqlik

- **G'olib:** U yaratgan `Book` modeli va `BookRepository` asosida kengaytma yozasan.
- **Azimbek:** Foydalanuvchi qidirgan kitob topilmasa, Azimbekning AI agentiga yo'naltiriladi.
- **Ozod:** Sening qidiruv endpointing Kiosk va Veb interfeyslarining asosiy yuragi bo'ladi.

---

## ✅ Qabul Mezonlari (Definition of Done)

- "alisher" yozilganda "Alisher Navoiy" kitoblari topiladi.
- "tarix" janri tanlanganda faqat tarixiy kitoblar filtrlanadi.
- Bo'sh natija berilganda `ask_ai: true` tavsiyasi qaytadi.
- Barcha qidiruvlar sahifalash (pagination) bilan ishlaydi.

---

## 🌿 Ishchi Branch

`sarvarbek/search`
