# OLLABERGANOV SARVARBEK DAVRONBEK O'G'LI — Qidiruv + Katalog

**Rol:** Eng ko'p ishlatiladigan funksiya seniki — tez va aniq qidiruv.

## Vazifalaring

- [ ] Qidiruv funksiyasi (backend yoki frontend-da, G'olib bilan kelishib):
  - nom bo'yicha: `alisher` yozsa "Alisher Navoiy" chiqsin
  - muallif bo'yicha
  - janr bo'yicha filtr: `fantastika, tarix, darslik, roman, ilmiy`
  - Katta-kichik harf farq qilmasin (`LOWER()` yoki `.lower()`)
- [ ] Natija kartochkasi: nom, muallif, janr, yil, javon (masalan: 2-qavat, A-3), holat (yashil=bo'sh, qizil=band)
- [ ] Sort: yangi kitoblar tepada, bo'shlari birinchi
- [ ] Bo'sh natijada: "Topilmadi, AI dan so'rang" degan tugma (Azimbek moduliga o'tadi)

## Texnik talab

- `GET /books?search=navoiy&janr=tarix` ni ishlatish
- So'rov 300ms dan sekin bo'lmasin (LIKE yetadi, murakkablashtirma)
- SQL injection dan himoya: f-string bilan query yig'ma, `?` parametr ishlat

## Bog'liqlik

- G'olib: `/books` endpointi
- Ozod: sening natijang uning kiosk ekranida chiqadi

## Qabul mezoni

- 3 harf yozilganda natija chiqadi
- "atosh" yozilganda ham "Otash" topiladi (case-insensitive)
- Band/bo'sh rangi to'g'ri ko'rinadi

## Branch

`sarvarbek/search`

## Birinchi qadam

G'olibdan 10 ta test kitobni ol, qidiruvni avval oddiy python funksiya qilib testla, keyin API ga ula.
