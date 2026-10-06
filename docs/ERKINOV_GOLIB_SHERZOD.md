# ERKINOV G'OLIB SHERZOD O'G'LI — Backend (Kitoblar Domeni)

**Rol:** Kitoblar domeni bo'yicha mas'ul backend muhandisi. Kitoblar ma'lumotlar bazasi, CRUD operatsiyalari va API qatlami.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **Model (`backend/app/models/book.py`):**
  - SQLAlchemy 2.0 `Book` modelini yaratish:
    - `id`: Integer (Primary Key)
    - `title`: String (kitob nomi)
    - `author`: String (muallif)
    - `genre`: String (janr)
    - `year`: Integer (nashr yili)
    - `shelf_location`: String (masalan: "2-qavat, A-3 javon")
    - `status`: String ("available" / "borrowed" / "reserved")
    - `description`: Text (ixtiyoriy qisqacha tavsif)
- [ ] **Sxemalar (`backend/app/schemas/book.py`):**
  - Pydantic modellar: `BookCreate`, `BookUpdate`, `BookResponse`
- [ ] **Repository (`backend/app/repositories/book_repo.py`):**
  - `get_by_id(db: AsyncSession, book_id: int) -> Optional[Book]`
  - `get_all(db: AsyncSession, skip: int, limit: int) -> List[Book]`
  - `create(db: AsyncSession, obj_in: BookCreate) -> Book`
  - `update(db: AsyncSession, db_obj: Book, obj_in: BookUpdate) -> Book`
  - `delete(db: AsyncSession, book_id: int) -> bool`
- [ ] **Xizmat qatlami (`backend/app/services/book_service.py`):**
  - Kitob qo'shish va yangilash bo'yicha biznes qoidalari.
  - Kitob mavjudligini tekshirish (mavjud bo'lmasa 404 xatosi).
- [ ] **API Endpointlari (`backend/app/api/v1/books.py`):**
  - `GET /api/v1/books` — kitoblar ro'yxati (pagination bilan)
  - `GET /api/v1/books/{id}` — bitta kitob haqida batafsil ma'lumot
  - `POST /api/v1/books` — yangi kitob qo'shish (Faqat Admin / Kutubxonachi uchun: `dependencies.check_role`)
  - `PUT /api/v1/books/{id}` — kitobni tahrirlash (Faqat Admin uchun)
  - `DELETE /api/v1/books/{id}` — kitobni o'chirish (Faqat Admin uchun)

---

## 🔗 Jamoaga Bog'liqlik

- **Ozodbek:** Senga `db/session.py` va xavfsizlik (`dependencies.py`) ni beradi.
- **Sarvarbek:** Sening `BookRepository`ingga qidiruv va filtrlash metodlarini qo'shadi.
- **Azimbek & Ozod:** Sening `/api/v1/books` endpointlaring orqali kitoblarni ko'radi.

---

## ✅ Qabul Mezonlari (Definition of Done)

- Kitoblar bo'yicha to'liq CRUD operatsiyalari Swagger `/docs` da ishlaydi.
- Admin bo'lmagan foydalanuvchi kitob qo'shmoqchi yoki o'chirmoqchi bo'lsa `403 Forbidden` qaytadi.
- Kitob topilmaganda chiroyli `404 Not Found` JSON javob qaytadi.

---

## 🌿 Ishchi Branch

`golib/books-core`
