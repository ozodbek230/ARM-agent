# Kutubxona Yordamchi Agenti (ARM)

Kutubxona kirishidagi katta ekranda fullscreen ishlaydigan **Kiosk** hamda masofadan kirish uchun **Web** gibrid tizimi.
Tizim Senior darajadagi **Qatlamli Arxitektura (Layered / Clean Architecture)** asosida qurilgan.

---

## 🏛 Texnologiya Staki (Production Standart)

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy 2.0 (Async), aiosqlite (SQLite)
- **Validatsiya & Sozlamalar:** Pydantic v2, Pydantic-Settings
- **Xavfsizlik:** JWT (python-jose), bcrypt (passlib)
- **Frontend:** Toza Web standartlari (HTML5, Modern CSS3, JavaScript ES6+) — Frameworklarsiz yengil va tezkor
- **AI Agent:** Gibrid arxitektura — Dastlab qoidaga asoslangan (rule-based tools), keyin LLM (Gemini / Ollama)
- **Testlash:** Pytest, pytest-asyncio, HTTPX

---

## 🏗 Arxitektura va Papkalar Tuzilmasi

Loyiha qat'iy **Mas'uliyatlar Taqsimoti (Separation of Concerns)** asosida quyidagi qatlamlarga bo'lingan:

```text
ARM/
├── .env.example                 # Muhit o'zgaruvchilari
├── .gitignore                   # Git istisnolari
├── requirements.txt             # Bog'liqliklar
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI ilovasi va global routerlar
│   │   ├── core/                # Sozlamalar (config), xavfsizlik (security), dependencies
│   │   ├── db/                  # Baza ulanishi (session), jadvallar (base), seed ma'lumotlar
│   │   ├── models/              # SQLAlchemy ma'lumotlar bazasi modellari
│   │   ├── schemas/             # Pydantic DTO (request va response modellari)
│   │   ├── repositories/        # Data Access Layer (faqat SQL / DB amallari)
│   │   ├── services/            # Biznes mantiq qatlami (Business Logic Layer)
│   │   │   └── ai_agent/        # Aqlli yordamchi agent moduli
│   │   └── api/
│   │       └── v1/              # API v1 endpoints (/auth, /books, /borrows, /agent)
│   └── tests/                   # Avtomatlashgan testlar (Pytest)
│
└── frontend/
    ├── shared/                  # Umumiy API mijoz va utilitlar
    ├── kiosk/                   # Kiosk interfeysi (Fullscreen, touch, 60s idle reset)
    └── web/                     # Talabalar/Foydalanuvchilar veb portali
```

---

## 👥 Jamoa va Rollar Taqsimoti

| # | Ism-familiya | Rol va Qatlam | Mas'ul bo'lgan moduli | Branch |
|---|---|---|---|---|
| 1 | **TO'XTAYEV OZODBEK** | **Team Lead & Core Arxitektor** | `core/`, `db/`, `models/user.py`, `schemas/auth.py`, `api/v1/auth.py`, Git boshqaruvi | `ozodbek/core-auth` |
| 2 | **ERKINOV G'OLIB** | **Backend (Kitoblar domeni)** | `models/book.py`, `schemas/book.py`, `repositories/book_repo.py`, `services/book_service.py`, `api/v1/books.py` | `golib/books-core` |
| 3 | **OLLABERGANOV SARVARBEK** | **Backend (Qidiruv & Filtr)** | Qidiruv va saralash: `repositories/book_repo.py` (qidiruv), `BookFilter` sxemasi, tezkor qidiruv | `sarvarbek/search` |
| 4 | **SHAHRIDDINOV NAVRO'ZBEK** | **Backend (Ijara & Bron)** | `models/borrow.py`, `schemas/borrow.py`, `repositories/borrow_repo.py`, `services/borrow_service.py`, `api/v1/borrows.py` | `navrozbek/booking` |
| 5 | **ABDUSALOMOV AZIMBEK** | **AI Agent Muhandisi** | `services/ai_agent/` (Agent mantiqi, promptlar, tools) va `api/v1/agent.py` | `azimbek/ai-agent` |
| 6 | **NE'MATULLAYEV OZOD** | **Frontend Muhandisi** | `frontend/kiosk/` va `frontend/web/` interfeyslari, `shared/api.js` integratsiyasi | `ozod/frontend` |
| 7 | **RAHIMBOYEV A'ZAMJON** | **QA & Texnik Hujjatlashtirish** | `backend/tests/` (Pytest testlari), Swagger verifikatsiyasi, loyiha hisoboti va taqdimot | `azamjon/qa-docs` |

---

## 📜 Git Qoidalari

1. `main` — faqat production-tayyor, testdan o'tgan barqaror kod.
2. Har bir a'zo o'z branchida ishlaydi: `git checkout -b <branch_nomi>`.
3. Commit xabarlari aniq va standart formatda:
   - `feat(books): kitoblar uchun repository va service qatlami qo'shildi`
   - `fix(auth): token muddatini tekshirish to'g'rilandi`
4. `main` ga birlashtirish faqat **Ozodbek (Team Lead)** orqali amalga oshiriladi.

---

## 🚀 Ishga Tushirish Bosqichlari (Roadmap)

1. **0-bosqich:** Skelet, `.env`, `core/`, `db/` va Auth poydevori (Ozodbek).
2. **1-bosqich:** Kitoblar va Qidiruv modullari (G'olib, Sarvarbek).
3. **2-bosqich:** Ijara, Bron qilish va AI Yordamchi (Navro'zbek, Azimbek).
4. **3-bosqich:** Kiosk va Veb interfeyslarini ulash (Ozod).
5. **4-bosqich:** Testlar, xatoliklarni bartaraf etish va hisobot (A'zamjon).

Batafsil topshiriqlar har bir a'zoning o'z faylida: `docs/<FAMILIYA>.md`.
