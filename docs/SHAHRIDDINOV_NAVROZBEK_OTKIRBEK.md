# SHAHRIDDINOV NAVRO'ZBEK O'TKIRBEK O'G'LI — Bron + Navbat + Web

**Rol:** Uydan kiradiganlar + bron tizimi seniki.

## Vazifalaring

- [ ] Bron API (G'olib bilan kelishib, yoki o'zing `backend/routes_booking.py` da):
  - `POST /reserve` — body: user_id, book_id. Band kitobga navbatga yozadi
  - `GET /reservations/{user_id}` — mening bronlarim
  - `DELETE /reservations/{id}` — bronni bekor qilish
- [ ] Qoida: bitta kitobga 3 kishidan ko'p navbat bo'lmasin
- [ ] Kitob bo'shaganda birinchi navbatdagiga "olib ketishingiz mumkin" statusi
- [ ] Web sahifa `frontend/web/index.html`:
  - Login sahifasi (Ozodbekning `/auth/login` ga ulanadi)
  - "Bron qilish" tugmasi (kioskda yo'q, faqat webda)
  - "Mening kitoblarim" sahifasi: olgan + bron qilganlar, qaytarish muddati
- [ ] Muddat eslatma: qaytarishga 2 kun qolganda sariq, o'tib ketsa qizil yozuv

## Texnik talab

- Login bo'lmasa bron qilib bo'lmaydi (token tekshir)
- Bir odam bitta kitobni 2 marta bron qilolmaydi (UNIQUE tekshiruvi)
- Sana formati: `YYYY-MM-DD` (masalan 2026-09-28)

## Bog'liqlik

- Ozodbek: `/auth/login`, users jadvali
- G'olib: `/borrow`, `/return`, books holati
- Ozod: kioskda "bron uydan qilinadi" degan yozuv chiqarishi uchun senga havola beradi

## Qabul mezoni

- Band kitobga bron qo'ysa navbatga tushadi
- 4-chi odamga "navbat to'la" xatosi chiqadi
- Login-siz kirsa bron tugmasi ishlamaydi

## Branch

`navrozbek/booking`

## Birinchi qadam

Avval `reservations` jadvalini Ozodbekdan so'ra, keyin postman yoki curl bilan `POST /reserve` ni testla, oxirida web sahifa qil.
