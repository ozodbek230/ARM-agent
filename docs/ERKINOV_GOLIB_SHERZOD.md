# ERKINOV G'OLIB SHERZOD O'G'LI — Backend API

**Rol:** Ozodbekning o'ng qo'li. API yadroni yozasan.

## Vazifalaring

- [ ] Ozodbek bergan `backend/db.py` ga ulanish (o'zing baza yaratma, uning bazasini ishlat)
- [ ] Endpointlar:
  - `GET /books?search=&janr=` — ro'yxat
  - `GET /books/{id}` — bitta kitob
  - `POST /books` — faqat admin (kitob qo'shish: nom, muallif, janr, javon)
  - `DELETE /books/{id}` — faqat admin
  - `POST /borrow` — body: user_id, book_id. Agar holat=bosh bo'lsa -> band qiladi + borrows ga yozadi
  - `POST /return` — body: book_id. band -> bosh qiladi
  - `GET /my-books/{user_id}` — kim nima olgani
- [ ] Xatolarni to'g'ri qaytarish: kitob topilmasa 404, band kitobga 400 `{"xato": "kitob band"}`
- [ ] `holat` maydonini doim yangilab borish (unutib ketma!)

## Texnik talab

- FastAPI, pydantic modellar: `BookCreate`, `BorrowRequest`
- Barcha funksiyalar `try/except` bilan, server yiqilmasin
- Ozodbekning auth tokenini tekshir: `admin` bo'lmasa `POST /books` ga ruxsat yo'q

## Bog'liqlik

- Ozodbek: baza + auth tayyor bo'lishini kutasan
- Sening API'ingga: Sarvarbek (qidiruv), Navro'zbek (bron), Ozod (UI) ulanadi

## Qabul mezoni

- `/docs` da barcha endpointlar ko'rinadi
- Band kitobni ikkinchi marta olib bo'lmaydi
- Qaytarilganda holat yana `bosh` bo'ladi

## Branch

`golib/api`

## Birinchi qadam

Ozodbekdan `db.sqlite3` yo'lini so'ra, keyin `backend/routes_books.py` ochib boshlagin.
