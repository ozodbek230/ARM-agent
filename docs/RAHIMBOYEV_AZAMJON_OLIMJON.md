# RAHIMBOYEV A'ZAMJON OLIMJON O'G'LI — QA & Texnik Hujjatlashtirish

**Rol:** Tizim sifatini nazorat qilish (QA), API testlari, loyihaning to'liq texnik hujjatlari va himoya taqdimoti bo'yicha mas'ul muhandis.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **API va Tizim Testlari (`backend/tests/`):**
  - Pytest va HTTPX yordamida asosiy test senariylarini yozish / tekshirish:
    - `test_auth.py` — ro'yxatdan o'tish, noto'g'ri parol, token olish.
    - `test_books.py` — kitob qo'shish, qidirish, admin ruxsati tekshiruvi.
    - Ijara va navbat testlari — band kitobni qayta ololmaslik, navbat chegarasi.
- [ ] **Swagger / OpenAPI nazorati:**
  - `http://127.0.0.1:8000/docs` manzilidagi barcha endpointlarning to'g'ri tavsiflangani, parametrlar va xatolik kodlari mavjudligini audit qilish.
- [ ] **Texnik Loyiha Hujjati (15-20 bet):**
  1. **Kirish:** Kutubxonadagi navbat va qidiruv muammolari, tizim maqsadi.
  2. **Tizim Arxitekturasi:** Qatlamli arxitektura chizmasi (Clean Architecture), modullar bog'liqligi.
  3. **Ma'lumotlar Bazasi Modeli:** ERD sxemasi (`users`, `books`, `borrows`, `reservations`).
  4. **API Spetsifikatsiyasi:** Endpointlar, parametrlar va qaytuvchi JSON javoblar jadvali.
  5. **Jamoa a'zolari hisoboti:** Har bir a'zo bajargan ishlar va ularning hissalari.
  6. **Sinov va Natijalar:** Test natijalari, Kiosk va Veb interfeyslarining skrinshotlari.
  7. **Xulosa va Rivojlantirish:** Tizimning kelajakdagi imkoniyatlari (RFID, to'liq LLM, telegram bot).
- [ ] **Loyiha Taqdimoti (Prezentatsiya - 10-12 slayd):**
  - Muammo -> Arxitektura va Yechim -> Jonli Demo ssenariysi -> Jamoa.
- [ ] **Demo Ssenariy:**
  - Loyihani himoya qilish vaqtida 3-5 daqiqada ko'rsatiladigan qat'iy qadamlar ketma-ketligini tayyorlash.

---

## 🔗 Jamoaga Bog'liqlik

- **Ozodbek:** Arxitektura sxemasi, baza ERD chizmasi va Git hisobotlari.
- **G'olib, Sarvarbek, Navro'zbek:** API endpointlari va xatolik javoblari.
- **Azimbek:** AI agentning test javoblari.
- **Ozod:** Kiosk va Veb interfeyslarining fotosuratlari va skrinshotlari.

---

## ✅ Qabul Mezonlari (Definition of Done)

- `pytest` buyrug'i barcha testlarni yashil (PASS) qilib o'tkazishi.
- Yakuniy hisobot hujjati to'liq rasmiylashtirilgan, barcha jamoa a'zolari qismlari kiritilgan bo'lishi.
- Jonli ko'rsatuv (Live demo) uchun ssenariy tayyor bo'lishi.

---

## 🌿 Ishchi Branch

`azamjon/qa-docs`
