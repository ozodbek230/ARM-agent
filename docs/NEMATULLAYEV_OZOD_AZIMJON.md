# NE'MATULLAYEV OZOD AZIMJON O'G'LI — Kiosk Frontend

**Rol:** Kutubxona kirishidagi katta ekrandagi chiroyli, katta tugmali interfeys seniki.

## Vazifalaring

- [ ] `frontend/kiosk/index.html` — fullscreen rejim:
  - Tepada: "KUTUBXONA YORDAMCHISI" + soat
  - O'rtada katta qidiruv input + 3 katta tugma: [Qidiruv] [Tavsiya] [Yordam]
  - Pastda: janr tugmalari (katta, barmoq sig'adigan: Tarix, Roman, Fantastika, Darslik)
- [ ] Touch-friendly: tugma kamida 64px, shrift kamida 20px
- [ ] Mehmon rejimi: login so'ralmaydi
- [ ] 60 soniya harakatsizlitsa avtomatik bosh sahifaga qaytish + input tozalash (JS `setTimeout`)
- [ ] Natija kartochka: kitob nomi katta, "2-qavat, A-3 javon" + yashil/qizil holat
- [ ] Chat oynasi: Azimbekning `/chat` ga savol yuborish

## Texnik talab

- Toza HTML/CSS/JS yetadi, framework shart emas
- `fetch('http://127.0.0.1:8000/books?search=...')` bilan backendga ulan
- Kiosk brauzerda F11 (fullscreen) da sinab ko'r
- Klaviatura bo'lmasa ham ishlasin (ekran klaviaturasi chiqsa yaxshi)

## Bog'liqlik

- G'olib: `/books` API
- Sarvarbek: qidiruv mantiqi
- Azimbek: `/chat` API

## Qabul mezoni

- 2 metr uzoqdan o'qiladi
- 60 sek teginilmasa reset bo'ladi
- Internet bo'lmasa ham local serverda ishlaydi

## Branch

`ozod/kiosk-ui`

## Birinchi qadam

`frontend/kiosk/` papka och, avval qog'ozga eskiz chiz, keyin 1 sahifalik html qil. Orqaga kutma — mock (soxta) kitoblar bilan boshla.
