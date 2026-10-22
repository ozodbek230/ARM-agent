# 🤖 4-AGENT: IJARA VA BRON DOMENI YAKUNIY HISOBOTI

`promptlar/4-agent.md` ko'rsatmalari to'liq va Clean / Layered Architecture tamoyillari asosida bajarildi. Ijara va Bron domeni — SQLAlchemy modellari, Pydantic v2 sxemalari, Repository, Service biznes mantiqi va REST API endpointlari muvaffaqiyatli amalga oshirildi.

---

## Yozilgan / Tahrirlangan fayllar:
| Fayl | Qator soni | Holat |
|---|---|---|
| backend/app/models/borrow.py | 84 | ✅ |
| backend/app/models/__init__.py | 17 | ✅ |
| backend/app/schemas/borrow.py | 53 | ✅ |
| backend/app/schemas/__init__.py | 47 | ✅ |
| backend/app/repositories/borrow_repo.py | 148 | ✅ |
| backend/app/services/borrow_service.py | 170 | ✅ |
| backend/app/api/v1/borrows.py | 113 | ✅ |
| backend/app/api/v1/router.py | 16 | ✅ |
| backend/tests/test_borrows.py | 260 | ✅ |
| **JAMI** | **~908** | ✅ |

---

## Hal etilgan 7 ta potensial muammo:
1. **Vaqt zonalari (timezone):** Barcha vaqtlar `datetime.now(timezone.utc)` va `timedelta(days=N)` bilan standart generatsiya qilindi.
2. **Navbat o'rni buzilib ketishi:** `shift_queue_positions()` metodi `UPDATE reservations SET queue_position = queue_position - 1 WHERE queue_position > :cancelled_pos AND status IN ('waiting', 'notified')` mantiqini qat'iy bajaradi.
3. **Boshqa foydalanuvchi ijarasini qaytarish:** Service qatlamida `borrow.user_id != current_user.id` tekshiruvi — admin/librarian bundan mustasno.
4. **Qayta qaytarish:** `borrow.status == "returned"` bo'lsa `BadRequestError("Ushbu kitob allaqachon qaytarilgan")` tashlanadi.
5. **4-odam navbat chegarasi:** Bron yaratishdan oldin `len(active_reservations) >= 3` tekshiruvi.
6. **Bo'sh kitobni bron qilish:** `book.status == "available"` bo'lsa `BadRequestError` qaytariladi.
7. **Test izolyatsiyasi:** `test_borrows.py` da teardown — borrows/reservations tozalanadi, kitoblar statuslari "available" ga qaytariladi. Bu oldingi 38 testning buzilishini oldini oldi.

---

## Test natijalari:
`pytest backend/tests/test_borrows.py -v`:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-8.3.3, pluggy-1.7.0
asyncio: mode=Mode.AUTO, default_loop_scope=function
collecting ... collected 14 items

backend/tests/test_borrows.py::test_borrow_available_book_success PASSED [  7%]
backend/tests/test_borrows.py::test_borrow_already_borrowed_book_fails PASSED [ 14%]
backend/tests/test_borrows.py::test_borrow_nonexistent_book_fails PASSED [ 21%]
backend/tests/test_borrows.py::test_borrow_unauthorized_fails PASSED     [ 28%]
backend/tests/test_borrows.py::test_return_book_success PASSED           [ 35%]
backend/tests/test_borrows.py::test_return_already_returned_book_fails PASSED [ 42%]
backend/tests/test_borrows.py::test_return_other_users_book_forbidden PASSED [ 50%]
backend/tests/test_borrows.py::test_get_my_borrows PASSED                [ 57%]
backend/tests/test_borrows.py::test_reserve_borrowed_book_success PASSED [ 64%]
backend/tests/test_borrows.py::test_reserve_available_book_fails PASSED  [ 71%]
backend/tests/test_borrows.py::test_duplicate_reservation_fails PASSED   [ 78%]
backend/tests/test_borrows.py::test_reservation_queue_max_limit PASSED   [ 85%]
backend/tests/test_borrows.py::test_return_book_notifies_first_in_queue PASSED [ 92%]
backend/tests/test_borrows.py::test_cancel_reservation_shifts_queue PASSED [100%]

====================== 14 passed, 32 warnings in 18.01s =======================
```

Umumiy testlar holati (`pytest -v`):
```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-8.3.3, pluggy-1.7.0
asyncio: mode=Mode.AUTO, default_loop_scope=function
collecting ... collected 52 items

backend/tests/test_auth.py   :: 14 tests  ✅
backend/tests/test_books.py  :: 12 tests  ✅
backend/tests/test_borrows.py:: 14 tests  ✅
backend/tests/test_search.py :: 12 tests  ✅

====================== 52 passed, 48 warnings in 27.27s =======================
```
(14 auth + 12 books + 14 borrows + 12 search = **52 ta test, barchasi 100% muvaffaqiyatli!**)

---

## 📌 5-AGENT (AI Agent — Rahimboyev A'zamjon) VA 6-AGENT (Frontend) UCHUN ESLATMA:
- **Kitob olish endpointi:** `POST /api/v1/borrows` → `{"book_id": N, "days": 14}`
- **Qaytarish endpointi:** `POST /api/v1/borrows/return` → `{"borrow_id": N}` yoki `{"book_id": N}`
- **Mening kitoblarim:** `GET /api/v1/borrows/my`
- **Muddati o'tgan:** `GET /api/v1/borrows/overdue` (Admin/Librarian)
- **Navbatga yozilish:** `POST /api/v1/borrows/reservations` → `{"book_id": N}`
- **Mening bronlarim:** `GET /api/v1/borrows/reservations/my`
- **Bronni bekor qilish:** `DELETE /api/v1/borrows/reservations/{reservation_id}`
- **Navbat chegarasi:** har bir kitob uchun maksimal **3 ta odam**.
- **5-agent (AI):** foydalanuvchiga kitob tavsiya qilganda `book.status` ni tekshirib:
  - `"available"` → `POST /api/v1/borrows` bilan ijaraga olishni tavsiya qil
  - `"borrowed"` yoki `"reserved"` → `POST /api/v1/borrows/reservations` bilan navbatga yozilishni taklif qil
- **BorrowStatus:** `active`, `returned`, `overdue`
- **ReservationStatus:** `waiting`, `notified`, `cancelled`, `completed`
- **Ishchi branch:** `navrozbek/booking`
