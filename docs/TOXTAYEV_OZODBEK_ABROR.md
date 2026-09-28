# TO'XTAYEV OZODBEK ABROR O'G'LI — Team Lead / Baza / Auth / Git

**Rol:** Loyiha kapitani. Zamin yaratib berasan, boshqalarga yo'l ochasan.

## Vazifalaring

- [ ] GitHub repo ochish, `README.md`, `.gitignore` (python, sqlite) qo'shish
- [ ] SQLite baza yaratish: `backend/db.sqlite3`
- [ ] 3 ta jadval:
```sql
users(id INTEGER PRIMARY KEY, full_name TEXT, login TEXT UNIQUE, password_hash TEXT, role TEXT);
-- role: admin, kutubxonachi, talaba, mehmon
books(id INTEGER PRIMARY KEY, nom TEXT, muallif TEXT, janr TEXT, yil INTEGER, javon TEXT, holat TEXT);
-- holat: bosh, band
borrows(id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, olingan_sana TEXT, qaytarish_sana TEXT, status TEXT);
reservations(id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, sana TEXT, status TEXT);
```
- [ ] Test ma'lumot: 10 ta kitob, 2 ta user (admin/admin123, talaba/1234) qo'shish
- [ ] Auth API:
  - `POST /auth/register` — login, parol, ism
  - `POST /auth/login` — token qaytaradi (boshida oddiy, keyin JWT)
  - `GET /auth/me` — kim kirganini tekshirish
- [ ] Parolni `hashlib.sha256` bilan saqlash (ochiq saqlama!)
- [ ] Rollarga ruxsat: faqat admin kitob qo'sha oladi, mehmon faqat qidira oladi
- [ ] Boshqalarning branchlarini `main` ga merge qilish

## Boshqalarga bog'liqlik

Sen zaminni bersang bo'ldi:
- G'olib senga qarab API yozadi
- Sarvarbek, Azimbek, Ozod, Navro'zbek sening `/books` va `/auth` endpointlaringga ulanadi

## Qabul mezoni

- `python backend/app.py` yonganda `http://127.0.0.1:8000/docs` ochiladi
- admin/admin123 bilan login bo'ladi
- `GET /books` bo'sh bo'lmasa ham 10 ta kitob qaytaradi

## Branch

`ozodbek/core-auth`

## Birinchi qadam

```bash
pip install fastapi uvicorn
mkdir backend
# backend/app.py + backend/db.py yarat, jadvallarni ishga tushir
```
