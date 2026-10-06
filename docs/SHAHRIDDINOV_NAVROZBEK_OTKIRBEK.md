# SHAHRIDDINOV NAVRO'ZBEK O'TKIRBEK O'G'LI — Backend (Ijara & Bron Domeni)

**Rol:** Kitoblarni ijaraga berish (Borrow), qaytarish (Return), oldindan band qilish (Reservation) va navbat boshqaruvi bo'yicha backend muhandisi.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **Modellar (`backend/app/models/borrow.py`):**
  - `Borrow` modeli:
    - `id`: Integer (PK)
    - `user_id`: Integer (FK -> users.id)
    - `book_id`: Integer (FK -> books.id)
    - `borrow_date`: DateTime (olingan vaqt)
    - `due_date`: DateTime (qaytarish oxirgi muddati, odatda +14 kun)
    - `returned_date`: Optional[DateTime]
    - `status`: String ("active", "returned", "overdue")
  - `Reservation` modeli:
    - `id`: Integer (PK)
    - `user_id`: Integer (FK -> users.id)
    - `book_id`: Integer (FK -> books.id)
    - `reserved_at`: DateTime
    - `queue_position`: Integer (navbatdagi o'rni, 1, 2, 3)
    - `status`: String ("waiting", "notified", "cancelled", "completed")
- [ ] **Sxemalar (`backend/app/schemas/borrow.py`):**
  - `BorrowCreate`, `BorrowResponse`, `ReturnRequest`
  - `ReservationCreate`, `ReservationResponse`
- [ ] **Repository (`backend/app/repositories/borrow_repo.py`):**
  - `create_borrow(db, user_id, book_id, days=14)`
  - `mark_as_returned(db, borrow_id)`
  - `create_reservation(db, user_id, book_id)`
  - `get_user_active_borrows(db, user_id)`
  - `get_book_queue(db, book_id)`
- [ ] **Xizmat qatlami (`backend/app/services/borrow_service.py`):**
  - Kitob band bo'lsa, uni ijaraga berishni bloklash (400 Bad Request).
  - Bitta kitob uchun maksimal 3 kishilik navbat chegarasi (agar navbat >= 3 bo'lsa, xato qaytarish).
  - Kitob qaytarilganda, agar navbatda odam bo'lsa, 1-o'rindagi bron statusini "notified" ga o'tkazish; agar navbat bo'lmasa kitob holatini "available" qilish.
  - Foydalanuvchining muddati o'tib ketgan kitoblarini aniqlash (overdue).
- [ ] **API Endpointlari (`backend/app/api/v1/borrows.py`):**
  - `POST /api/v1/borrows` — kitob olish (avtorizatsiyadan o'tgan foydalanuvchi)
  - `POST /api/v1/borrows/return` — kitob qaytarish
  - `GET /api/v1/borrows/my` — mening kitoblarim (joriy foydalanuvchi uchun)
  - `POST /api/v1/reservations` — band kitobga navbatga yozilish
  - `DELETE /api/v1/reservations/{id}` — bronni bekor qilish

---

## 🔗 Jamoaga Bog'liqlik

- **Ozodbek:** Senga `User` modelini va `get_current_user` autentifikatsiya dependency'sini beradi.
- **G'olib:** Senga `Book` modelini beradi (ijara paytida kitob statusi o'zgaradi).
- **Ozod:** Sening API'laringni Veb interfeysidagi shaxsiy kabinetga ulaydi.

---

## ✅ Qabul Mezonlari (Definition of Done)

- Bo'sh kitob ijaraga olinganda kitob holati avtomatik "borrowed" ga aylanadi.
- Band kitob olinmoqchi bo'lsa ruxsat bermaydi, faqat navbatga yozilish imkoni bo'ladi.
- 4-chi odam bron qilmoqchi bo'lsa "Navbat to'lgan" xatosi chiqadi.
- Qaytarish sanasi o'tib ketgan kitoblar "overdue" sifatida belgilanadi.

---

## 🌿 Ishchi Branch

`navrozbek/booking`
