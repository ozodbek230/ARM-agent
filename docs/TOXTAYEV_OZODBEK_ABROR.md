# TO'XTAYEV OZODBEK ABROR O'G'LI — Team Lead & Core Arxitektor

**Rol:** Loyiha arxitektori va yetakchisi. Tizim yadrosi, xavfsizlik, baza poydevori va jamoa kodini nazorat qilish.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] Loyiha skeletini, `.gitignore`, `requirements.txt` va `.env.example` sozlamalarini tasdiqlash
- [ ] **Core qatlami (`backend/app/core/`):**
  - `config.py` — Pydantic Settings orqali konfiguratsiya boshqaruvi
  - `security.py` — Parollarni bcrypt orqali xeshlash, JWT token yaratish va dekodlash
  - `dependencies.py` — FastAPI Dependency Injection: `get_db()`, `get_current_user()`, `check_role(["admin", "librarian"])`
  - `exceptions.py` — Tizim bo'yicha yagona xatoliklar (Custom HTTP Exceptions)
- [ ] **Baza poydevori (`backend/app/db/`):**
  - `session.py` — SQLAlchemy `AsyncSession` va engine yaratish
  - `base.py` — Barcha SQLAlchemy modellarni ro'yxatdan o'tkazish va jadvallarni avtomatik yaratish (`init_db`)
  - `seed.py` — Dastlabki 10 ta kitob va 2 ta foydalanuvchi (admin va talaba) ni bazaga kiritish
- [ ] **Foydalanuvchi va Auth domeni:**
  - `models/user.py` — `User` modeli (`id`, `full_name`, `login`, `password_hash`, `role`, `created_at`)
  - `schemas/user.py`, `schemas/auth.py` — `UserCreate`, `UserResponse`, `Token`, `LoginRequest`
  - `repositories/user_repo.py` — Foydalanuvchini bazadan qidirish va saqlash
  - `services/auth_service.py` — Ro'yxatdan o'tish va autentifikatsiya biznes mantiqi
  - `api/v1/auth.py` — `/auth/register`, `/auth/login`, `/auth/me` endpointlari
- [ ] **Git & Code Review:**
  - Jamoa a'zolarining pull requestlarini tekshirish va `main` branchga merge qilish

---

## 🔗 Jamoaga Bog'liqlik

- **G'olib va Navro'zbek:** Sening `session.py` va `Base` modelingga qarab o'z modellarini yozadi.
- **Azimbek va Ozod:** Sening `/auth/login` va JWT tokening orqali tizimga ulanadi.

---

## ✅ Qabul Mezonlari (Definition of Done)

- `uvicorn backend.app.main:app --reload` yurganda xatoliksiz ishga tushadi.
- `http://127.0.0.1:8000/docs` da Swagger UI to'liq ochiladi.
- `/api/v1/auth/login` orqali admin (admin / admin123) login qilganda JWT token qaytadi.
- `/api/v1/auth/me` orqali joriy foydalanuvchi ma'lumotlari to'g'ri olinadi.

---

## 🌿 Ishchi Branch

`ozodbek/core-auth`
