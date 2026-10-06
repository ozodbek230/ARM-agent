# ARM — Axborot Resurs Markazi (Kutubxona Yordamchi Agenti)

Avtomatlashtirilgan Axborot-Kutubxona Tizimi — Kutubxona kirishidagi sensorli katta ekran (**Kiosk**) hamda masofaviy foydalanuvchilar (**Web**) uchun gibrid tizim.

Loyiha sanoat standarti bo'lgan **Qatlamli Arxitektura (Layered / Clean Architecture)** asosida ishlab chiqilgan.

---

## 🚀 Loyihani Ishga Tushirish

### 1. Virtual muhitni faollashtirish va kutubxonalarni o'rnatish:

```bash
# Virtual muhit yaratish
python3 -m venv venv

# Faollashtirish (Linux/macOS)
source venv/bin/activate
# Windows uchun:
# venv\Scripts\activate

# Kerakli paketlarni o'rnatish
pip install -r requirements.txt
```

### 2. Muhit o'zgaruvchilari sozlamalari:

```bash
cp .env.example .env
```

### 3. Serverni ishga tushirish:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

* **Swagger API Hujjatlari:** `http://127.0.0.1:8000/docs`
* **Kiosk Interfeysi:** `frontend/kiosk/index.html`
* **Veb Portal:** `frontend/web/index.html`

---

## 📚 Loyiha Hujjatlari va Jamoa Taqsimoti

Barcha texnik topshiriqlar, arxitektura qoidalari va har bir a'zoning vazifalari `docs/` papkasida joylashgan:

* 📖 [Umumiy Arxitektura va Jamoa Rejasi](docs/README.md)
* 👤 [To'xtayev Ozodbek (Team Lead & Core Arxitektor)](docs/TOXTAYEV_OZODBEK_ABROR.md)
* 👤 [Erkinov G'olib (Backend - Kitoblar)](docs/ERKINOV_GOLIB_SHERZOD.md)
* 👤 [Ollaberganov Sarvarbek (Backend - Qidiruv & Filtr)](docs/OLLABERGANOV_SARVARBEK_DAVRONBEK.md)
* 👤 [Shahriddinov Navro'zbek (Backend - Ijara & Bron)](docs/SHAHRIDDINOV_NAVROZBEK_OTKIRBEK.md)
* 👤 [Abdusalomov Azimbek (AI Agent Muhandisi)](docs/ABDUSALOMOV_AZIMBEK_TOIR.md)
* 👤 [Ne'matullayev Ozod (Frontend Muhandisi)](docs/NEMATULLAYEV_OZOD_AZIMJON.md)
* 👤 [Rahimboyev A'zamjon (QA & Hujjatlashtirish)](docs/RAHIMBOYEV_AZAMJON_OLIMJON.md)
