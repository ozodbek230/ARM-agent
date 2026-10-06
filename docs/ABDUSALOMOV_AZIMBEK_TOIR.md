# ABDUSALOMOV AZIMBEK TOIR O'G'LI — AI Agent Muhandisi

**Rol:** Kitobxonlarga kutubxona bo'yicha aqlli maslahat beruvchi, kitob tavsiya qiluvchi va yo'naltiruvchi AI agent arxitekturasi bo'yicha mas'ul muhandis.

---

## 🎯 Asosiy Mas'uliyatlar

- [ ] **Agent Papkasi (`backend/app/services/ai_agent/`):**
  - `prompts.py` — Kutubxona agentining shaxsiyati (System Prompt): do'stona, o'zbek tilida, faqat kutubxonadagi real kitoblarni tavsiya qiluvchi ko'rsatmalar.
  - `tools.py` — Agent uchun yordamchi vositalar (Function Calling / Tool Calling):
    - `tool_search_books(genre, keywords)` — ma'lumotlar bazasidan real kitoblarni qidirish.
    - `tool_check_availability(book_id)` — kitobning javon joylashuvi va bo'sh/bandligini bilish.
    - `tool_library_faq(question_type)` — ish vaqti, a'zolik qoidalari haqida ma'lumot berish.
  - `agent.py` — Yadro mantiqi:
    - 1-bosqich: Qoidaga asoslangan (Rule-based / Keyword matcher) va Tool integratsiyasi.
    - 2-bosqich: Gemini API (yoki mahalliy model) bilan ulanish imkoniyati (Fallback rejim bilan).
- [ ] **Sxemalar (`backend/app/schemas/ai.py` yoki `common.py`):**
  - `ChatRequest`: `message: str`, `session_id: Optional[str]`, `user_id: Optional[int]`
  - `ChatResponse`: `response_text: str`, `recommended_books: List[BookResponse]`, `suggested_actions: List[str]`
- [ ] **API Endpointi (`backend/app/api/v1/agent.py`):**
  - `POST /api/v1/agent/chat` — xabarni qabul qilish va agent javobini qaytarish.
- [ ] **Holat (Memory) boshqaruvi:**
  - Kioskda yoki vebda foydalanuvchining so'nggi 3-5 ta savol-javob kontekstini sessiyada saqlash.

---

## 🔗 Jamoaga Bog'liqlik

- **Ozodbek:** Senga baza va `Book` obyektlarini beradi.
- **G'olib & Sarvarbek:** Sening agenting ularning `search_books` metodidan kitoblarni tavsiya qilish uchun foydalanadi (Uydirma/hallyutsinatsiya kitoblar taqiqlanadi!).
- **Ozod:** Kiosk ekranidagi suhbat oynasini sening `/api/v1/agent/chat` endpointingga ulaydi.

---

## ✅ Qabul Mezonlari (Definition of Done)

- "Menga dasturlash bo'yicha qanday kitob bor?" deb so'ralganda, bazadagi IT darsliklarini va ularning javonini ko'rsatadi.
- Mavjud bo'lmagan kitob so'ralsa: "Kechirasiz, hozir bu kitob yo'q, lekin quyidagi o'xshash kitoblarni tavsiya qilaman" deydi.
- Javob berish vaqti 2 soniyadan oshmasligi kerak.

---

## 🌿 Ishchi Branch

`azimbek/ai-agent`
