# NE'MATULLAYEV OZOD AZIMJON O'G'LI — Frontend Muhandisi

**Rol:** Kutubxona kirishidagi Kiosk sensorli ekrani va talabalar uchun Veb portal interfeyslari bo'yicha mas'ul frontend muhandisi.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **Umumiy API mijoz (`frontend/shared/api.js`):**
  - Backend API (`/api/v1`) bilan ishlovchi sodda va ishonchli `fetch` wrapper.
  - Xatoliklarni ushlash va JSON formatida qaytarish.
- [ ] **Kiosk Interfeysi (`frontend/kiosk/`):**
  - `index.html`, `styles/kiosk.css`, `scripts/kiosk.js`
  - **Fullscreen (Sensorli ekran) dizayni:**
    - Katta va qulay tugmalar (kamida 60-70px balandlikda).
    - Aniq va yorqin shriftlar (2 metr masofadan bemalol o'qiladigan).
    - Bosh sahifada: Katta qidiruv paneli, Janrlar bo'yicha tezkor tugmalar, "AI Maslahatchi" tugmasi.
  - **Avtomatik qaytish (Idle Auto-Reset):**
    - Agar foydalanuvchi ekranga 60 soniya davomida tegmasa (sichqoncha/touch harakati bo'lmasa), interfeys avtomatik bosh holatiga qaytishi va qidiruv tozalanishi kerak (`setTimeout` orqali).
  - **AI Chat interfeysi:**
    - Kioskda ochiluvchi qulay modal suhbat oynasi (Azimbekning agentiga ulanadi).
- [ ] **Veb Portal (`frontend/web/`):**
  - `index.html`, `styles/web.css`, `scripts/web.js`
  - Moslashuvchan (Responsive — telefon va noutbuklar uchun) dizayn.
  - Foydalanuvchi avtorizatsiyasi (Login / Register modal).
  - Kitoblarni ko'rish, qidirish, band qilish va "Mening kitoblarim" bo'limi.

---

## 🔗 Jamoaga Bog'liqlik

- **Ozodbek:** Auth API (`/api/v1/auth/login`, token saqlash `localStorage` da).
- **G'olib & Sarvarbek:** Kitoblar ro'yxati va qidiruv API (`/api/v1/books`).
- **Navro'zbek:** Bron qilish va navbat API (`/api/v1/borrows`, `/api/v1/reservations`).
- **Azimbek:** AI Chat API (`/api/v1/agent/chat`).

---

## ✅ Qabul Mezonlari (Definition of Done)

- Kiosk brauzerda F11 (Fullscreen) rejimida buzilmasdan, chiroyli ochiladi.
- Qidiruv natijalarida kitobning joylashuvi (masalan: "2-qavat, 4-javon") va holati (yashil=bo'sh, qizil=band) aniq ko'rinadi.
- Kioskda 60 soniya tegilmasa, o'z-o'zidan bosh holatga qaytadi.
- Veb sahifada login qilgach, kitobni bron qilish tugmasi ishlaydi.

---

## 🌿 Ishchi Branch

`ozod/frontend`
