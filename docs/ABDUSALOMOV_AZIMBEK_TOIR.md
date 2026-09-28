# ABDUSALOMOV AZIMBEK TOIR O'G'LI — AI Chat Agent

**Rol:** "Menga qiziqarli kitob tavsiya qil" deganga aqlli javob beradigan yordamchi.

## Vazifalaring

- [ ] `POST /chat` endpointi: body `{"savol": "...", "user_id": 1}`
- [ ] Boshida qoida-based mantiq (LLM shart emas):
  - savolda `fantastika` bo'lsa -> janr=fantastika kitoblarni tavsiya qil
  - `imtihon, dars, fizika, tarix` bo'lsa -> darsliklarni ber
  - `zerikdim, qiziqarli, roman` bo'lsa -> romanlarni ber
  - hech narsa topilmasa -> "Kutubxonachidan so'rang" de
- [ ] Javob formati: `{"javob": "...", "kitoblar": [id1, id2, id3]}`
- [ ] Tarixni eslab qolish (oddiy): oxirgi 5 savolni xotirada saqla
- [ ] Keyin (vaqt qolsa): Ollama / OpenAI ulash uchun joy qoldir (`ai_provider.py` alohida fayl bo'lsin)

## Texnik talab

- Bazadan real kitob olish shart — o'zingdan to'qima ("Uydirma kitob" taqiqlanadi!)
- Agar baza bo'sh qaytsa, yolg'on tavsiya berma
- Javob o'zbekcha, qisqa, 2-3 gap + 3 ta kitob ro'yxati

## Bog'liqlik

- Ozodbek: baza
- G'olib: `/books` orqali kitob olish
- Sarvarbek: topilmaganda senga yo'naltiradi
- Ozod: sening javobing kiosk chat oynasida chiqadi

## Qabul mezoni

- "menga fantastika qiziq" -> 3 ta fantastika kitob qaytaradi
- Mavjud bo'lmagan kitobni tavsiya qilmaydi
- Server 2 soniyadan tez javob beradi

## Branch

`azimbek/ai-chat`

## Birinchi qadam

`backend/ai_agent.py` och, `def javob_ber(savol: str)` funksiyadan boshla, keyword lug'at tuz.
