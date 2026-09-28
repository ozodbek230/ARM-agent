# Kutubxona Yordamchi Agenti

Kutubxona kirishidagi katta ekranda fullscreen ishlaydigan **Kiosk + Web** gibrid tizim.
Mehmon login-siz qidiradi, ro'yxatdan o'tgan foydalanuvchi uydan ham kirib bron qiladi.

## Texnologiya (standart, yengil)

- **Backend:** Python 3.10+ , FastAPI, SQLite
- **Frontend:** HTML + CSS + JS (keyin Streamlit emas, toza web — kiosk uchun qulay)
- **AI Agent:** boshida qoida-based tavsiya, keyin LLM ulanadi
- **Git:** GitHub, har kim o'z branchida

## Arxitektura

```
[ Kiosk Ekran (fullscreen browser) ] \
                                       >-- [ FastAPI ] --> [ SQLite ]
[ Telefon / Uy kompyuteri (web) ]     /
```

Baza jadvallari: `books`, `users`, `borrows`, `reservations`

## Jamoa

| # | Ism | Rol | Branch |
|---|-----|-----|--------|
| 1 | TO'XTAYEV OZODBEK ABROR O'G'LI | Team Lead, Baza, Auth, Git | `ozodbek/core-auth` |
| 2 | ERKINOV G'OLIB SHERZOD O'G'LI | Backend API | `golib/api` |
| 3 | OLLABERGANOV SARVARBEK DAVRONBEK O'G'LI | Qidiruv + Katalog | `sarvarbek/search` |
| 4 | ABDUSALOMOV AZIMBEK TOIR O'G'LI | AI Chat Agent | `azimbek/ai-chat` |
| 5 | NE'MATULLAYEV OZOD AZIMJON O'G'LI | Kiosk Frontend | `ozod/kiosk-ui` |
| 6 | SHAHRIDDINOV NAVRO'ZBEK O'TKIRBEK O'G'LI | Bron + Navbat + Web | `navrozbek/booking` |
| 7 | RAHIMBOYEV A'ZAMJON OLIMJON O'G'LI | Hisobotchi (kod yozmaydi) | - |

## Git qoida

1. `main` — faqat ishlaydigan kod
2. Har kim: `git checkout -b <branch>` qilib ishlaydi
3. `main` ga merge faqat Ozodbek tasdiqlagach
4. Har commit qisqa va aniq: `kitob qidiruv qo'shildi`, `auth login tayyor`

## MVP bosqichlari

1. **Hafta 1:** Baza + API skelet + bo'sh UI (Ozodbek + G'olib)
2. **Hafta 2:** Qidiruv + Kiosk UI + Bron
3. **Hafta 3:** AI Chat + QR + test + hisobot

## Papka rejasi (keyin kod yozilganda)

```
/docs - shu hujjatlar
/backend - FastAPI + db.sqlite3
/frontend/kiosk - fullscreen UI
/frontend/web - uydan kirish UI
```

Har kim o'z vazifasini `docs/<FAMILIYA>.md` dan o'qiydi.
