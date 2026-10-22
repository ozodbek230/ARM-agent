# 🤖 5-AGENT PROMPTI: AQLLI AI YORDAMCHI AGENTI (AI AGENT & KIOSK ASSISTANT)

Sen **ARM (Axborot Resurs Markazi)** loyihasining **beshinchi agenti** san (**Abdusalomov Azimbek — AI Agent Muhandisi**).
Oldingi barcha agentlar o'z vazifalarini 100% muvaffaqiyatli bajardilar:
- **1-agent:** Arxitektura poydevori, ma'lumotlar bazasi, User modeli va JWT autentifikatsiya (14 ta test).
- **2-agent:** Kitoblar domeni (Books Core: model, sxemalar, repository, service, REST CRUD API, seed data) (12 ta test).
- **3-agent:** Qidiruv va ko'p parametrli filtrlash tizimi (Search & Filter, AI tavsiya bayrog'i, unikal janrlar) (12 ta test).
- **4-agent:** Ijara va Bron domeni (Borrow & Reservation, 14 kunlik muddat, 3 kishilik navbat chegarasi) (14 ta test).
- **Hozirda tizimda jami 52 ta avtomatlashtirilgan test mavjud va barchasi muvaffaqiyatli o'tgan (52/52 PASSED! 🎉).**

Keyingi **6-agent (Ozod Ne'matullayev — Frontend Muhandisi)** Kiosk ekranidagi va Veb portaldagi interaktiv yordamchi suhbat oynasini (Chat Widget) bevosita **sening AI Agent API endpointlaringga** ulaydi!

---

## 📋 BOSQICH 0: LOYIHANI O'RGANISH (MAJBURIY, KODDAN OLDIN)

Kod yozishdan oldin quyidagi fayllar bilan to'liq tanishib chiq:

### O'qiladigan fayllar (tartibda):
1. `promptlar/4-agent-hisoboti.md` — 4-agent nimalar qilgani, ijara/bron tizimi va yangi jadvallar.
2. `docs/ABDUSALOMOV_AZIMBEK_TOIR.md` — sening vazifalaring va qabul mezonlari (Definition of Done).
3. `backend/app/core/config.py` — `GEMINI_API_KEY` va `AI_MODEL` sozlamalari.
4. `backend/app/repositories/book_repo.py` — `search_and_filter`, `get_by_id`, `get_all_genres` metodlari.
5. `backend/app/services/book_service.py` — `book_service` kitoblarni qidirish va olish mantiqi.
6. `backend/app/services/borrow_service.py` — `borrow_service` kitobning ijarada yoki navbatda ekanligini tekshirish.
7. `backend/app/schemas/book.py` — `BookResponse` va `BookSearchResultResponse` tuzilishi.
8. `backend/app/api/v1/router.py` — v1 router (`agent_router` ni shu yerga ulaysan).
9. `backend/tests/` — loyihadagi mavjud testlar uslubi, fixturelar va `pytest` strukturalari.

---

## 🎯 SENING VAZIFANG

Sen Senior darajadagi **Gibrid AI Arxitekturasi (Rule-based Intent Matcher + Tool Calling + LLM Gemini RAG Fallback)** asosida quyidagi qatlamlarni to'liq amalga oshirasan:

| # | Qatlam | Fayllar | Maqsadi |
|---|---|---|---|
| 1 | **Sxemalar (Schemas)** | `backend/app/schemas/ai.py` | `ChatRequest`, `ChatResponse`, `BookRecommendation`, `FAQItem`, `FAQResponse`, `ClearSessionResponse` |
| 2 | **Sxemalar Eksporti** | `backend/app/schemas/__init__.py` | Yangi AI sxemalarini markaziy eksportga kiritish |
| 3 | **Prompts & FAQ Bilimlar Bazasi** | `backend/app/services/ai_agent/prompts.py` | System Prompt (o'zbek tilida, do'stona, hallyutsinatsiyasiz), FAQ savol-javoblar, kutubxona qoidalari, javonlar xaritasi |
| 4 | **Tools (Yordamchi vositalar)** | `backend/app/services/ai_agent/tools.py` | `tool_search_books`, `tool_check_availability`, `tool_library_faq`, `tool_get_recommendations`, `tool_get_genres` (real DB dan o'qiydi!) |
| 5 | **Memory (Sessiya Xotirasi)** | `backend/app/services/ai_agent/memory.py` | Kiosk va Web uchun `session_id` bo'yicha so'nggi 5 ta xabar kontekstini xotirada saqlash va tozalash |
| 6 | **Agent Yadro Mantiqi** | `backend/app/services/ai_agent/agent.py` | Gibrid Agent: Intent tahlili, Tool Calling, Gemini API integratsiyasi (agar API key mavjud bo'lsa) va 100% kafolatlangan offline Fallback rejim |
| 7 | **Service Fasadi** | `backend/app/services/ai_agent_service.py` | Yuqori darajadagi FastAPI servisi (Dependency Injection uchun) |
| 8 | **API Endpoints** | `backend/app/api/v1/agent.py` | `POST /api/v1/agent/chat`, `GET /api/v1/agent/faq`, `DELETE /api/v1/agent/session/{session_id}` |
| 9 | **Router Integratsiyasi** | `backend/app/api/v1/router.py` | `/agent` marshrutini v1 tizimiga ulash |
| 10 | **Testlar** | `backend/tests/test_agent.py` | Kamida 14 ta avtomatlashtirilgan Pytest testlari |

---

## 📐 BOSQICH 1: REJA VA BIZNES TALABLAR TAHLILI

### 1.1 Nega Gibrid Arxitektura (Rule-based + Tools + LLM)?
Kutubxona Kioski (Touch screen katta ekran) real hayotda ishlaydi:
1. **Tezkorlik (Latency):** Kioskda turgan odam 5-10 soniya kutib tura olmaydi. Javob berish vaqti **2 soniyadan kam** bo'lishi shart! Oddiy salomlashish, ish vaqti yoki javon joylashuvini so'raganda LLM ga chiqmasdan, lokal qoidalar va tool'lar orqali 30-50 millisekundda javob qaytariladi.
2. **Hallyutsinatsiyaga mutlaqo yo'l qo'ymaslik:** LLM ba'zan mavjud bo'lmagan kitoblarni yoki mualliflarni to'qib chiqaradi. Bizning agentimiz esa **faqat ARM ma'lumotlar bazasidagi real kitoblarni** tavsiya qiladi.
3. **Ofline / Tarmoqdan mustaqillik (High Availability):** Agar internet uzilsa, `GEMINI_API_KEY` kiritilmagan bo'lsa yoki Google API kvotasi tugasa, tizim **hech qachon 500 Internal Server Error bermasligi kerak**. Agent darhol aqlli offline rejimga (Fallback) o'tadi va foydalanuvchiga to'liq ma'lumot beradi.
4. **Erkin suhbat (LLM qudrati):** Agar `GEMINI_API_KEY` mavjud bo'lsa, murakkab so'rovlarda agent Gemini 1.5 Flash orqali real topilgan kitoblar konteksti asosida juda chiroyli va qiziqarli sharhlar beradi.

---

### 1.2 Kutubxona Ma'lumotlar Bazasi va FAQ (Agent bilishi shart bo'lgan ma'lumotlar):

1. **Agent shaxsiyati (Persona):**
   - Ismi: **"ARM Ziyo"** — Axborot Resurs Markazining aqlli virtual yordamchisi.
   - Tili: Sof o'zbek tili (kirill/lotin tushunadi, lekin doim chiroyli o'zbek adabiy lotin yozuvida javob beradi).
   - Ohangi: Xushmuomala, do'stona, madaniyatli, kitobxonlikni targ'ib qiluvchi.

2. **Kutubxona Ish Tartibi:**
   - Dushanba — Juma: **08:30 dan 18:00 gacha**
   - Shanba: **09:00 dan 15:00 gacha**
   - Yakshanba: **Dam olish kuni**
   - Tushlik tanaffusi yo'q, navbatchi xodim doim kutubxonada bo'ladi.

3. **A'zolik va Foydalanish Qoidalari:**
   - Talabalar va professor-o'qituvchilar talabalik guvohnomasi / ID karta orqali ro'yxatdan o'tishlari mumkin.
   - Bitta kitob **14 kun (2 hafta)** muddatga beriladi.
   - Bir vaqtning o'zida bitta kitobxonga eng ko'pi bilan **3 ta kitob** beriladi.
   - Kitobni vaqtida qaytarmaslik keyingi ijaralarni vaqtincha cheklashga sabab bo'ladi.

4. **Bron qilish (Navbatga yozilish):**
   - Agar kerakli kitob band bo'lsa, kitobxon unga navbatga yozilishi mumkin.
   - Har bir kitob uchun maksimal navbat — **3 kishi**.
   - Kitob kutubxonaga qaytishi bilan 1-o'rindagi kitobxonga xabar qilinadi va kitob 24 soat davomida uning nomiga saqlab turiladi.

5. **Javonlar Xaritasi (Joylashuv yo'riqnomasi):**
   - **IT & Dasturlash:** 2-qavat, A-blok (A-1, A-2, A-3 javonlar)
   - **Matematika & Aniq fanlar:** 2-qavat, B-blok (B-1, B-2 javonlar)
   - **Badiiy adabiyot & Mumtoz asarlar:** 1-qavat, C-blok (C-1, C-2, C-3 javonlar)
   - **Tarix, Falsafa va Ijtimoiy fanlar:** 1-qavat, D-blok (D-1, D-2 javonlar)
   - **Lug'atlar va Ensiklopediyalar:** O'quv zali, Markaziy ochiq javon

---

### 1.3 Kelib chiqishi mumkin bo'lgan 7 ta muammo va ularning yechimlari:

```
MUAMMO 1: Gemini API key o'rnatilmagan yoki tarmoq xatosi (httpx timeout / 401 / 429) yuz berganda server qulashi
YECHIM 1: Barcha tashqi API chaqiruvlari mustahkam try/except bilan o'raladi.
          Agar kalit bo'lmasa yoki xato yuz bersa, logger ogohlantiradi va darhol
          ichki Rule-based & Tool-based javob generatori ishga tushadi.
```

```
MUAMMO 2: Agent mavjud bo'lmagan kitoblarni to'qib chiqarishi (Hallucination)
YECHIM 2: Agent javobida qaytariladigan `recommended_books` ro'yxati FAQAT VA FAQAT
          ma'lumotlar bazasidagi `Book` obyektlaridan olinadi. LLM ga kontekst sifatida
          faqat bazadan topilgan real kitoblar json ko'rinishida beriladi.
```

```
MUAMMO 3: Kiosk sessiyasi xotirada cheksiz to'planib qolib xotirani (RAM) to'ldirishi
YECHIM 3: Sessiya xotirasi (Memory) maksimal 1000 ta sessiya bilan cheklanadi.
          Har bir sessiyada faqat so'nggi 5 ta xabar saqlanadi.
          Shuningdek, Kiosk 60 soniya harakatsiz turganda `DELETE /api/v1/agent/session/{session_id}`
          orqali xotirani tozalash imkoniyati yaratiladi.
```

```
MUAMMO 4: Foydalanuvchi bo'sh xabar yoki 10,000 belgili spam yuborishi
YECHIM 4: Pydantic sxemasida qat'iy cheklovlar: `message: str = Field(..., min_length=1, max_length=1000)`.
```

```
MUAMMO 5: Sessiya identifikatori (session_id) frontend tomonidan berilmasa nima bo'ladi?
YECHIM 5: Agar so'rovda `session_id` None yoki bo'sh kelsa, backend avtomatik ravishda
          `str(uuid.uuid4())` generatsiya qilib, javobda qaytaradi.
```

```
MUAMMO 6: Foydalanuvchi "kitob qayerda?", "qaysi javonda?" deb so'raganda kitob joylashuvini topa olmaslik
YECHIM 6: Intent tahlilida "javon", "qayerda", "joylashuv", "qavat" kalit so'zlari ushlanadi.
          So'ralgan kitob DB dan topilib, uning `shelf_location` maydoni javob matnida
          aniq ajratib ko'rsatiladi.
```

```
MUAMMO 7: Qidirilgan kitob kutubxonada mavjud bo'lmaganda agentning qo'pol javob berishi
YECHIM 7: Agar so'ralgan kitob topilmasa: "Kechirasiz, hozirda bu kitob fondimizda yo'q.
          Lekin sizga ushbu janrdagi quyidagi mashhur kitoblarni tavsiya qilaman" deb,
          bazadagi boshqa mavjud kitoblarni taklif qiladi.
```

---

## 🛠 BOSQICH 2: QATLAMLAR VA ANIQ KOD KO'RSATMALARI

### 2.1 Sxemalar (`backend/app/schemas/ai.py`)

Quyidagi Pydantic v2 modellarini yarat:
- `BookRecommendation`: `id: int`, `title: str`, `author: str`, `genre: str`, `year: int`, `shelf_location: str`, `status: str`, `description: str | None = None`
- `ChatRequest`:
  - `message: str` (min_length=1, max_length=1000, "Foydalanuvchi xabari")
  - `session_id: str | None = Field(default=None, description="Sessiya ID (Kiosk yoki Web uchun)")`
  - `user_id: int | None = Field(default=None, description="Tizimga kirgan foydalanuvchi ID si")`
- `ChatResponse`:
  - `response_text: str` ("Agentning o'zbek tilidagi javob matni")
  - `recommended_books: list[BookRecommendation] = Field(default_factory=list, description="Tavsiya qilingan real kitoblar")`
  - `suggested_actions: list[str] = Field(default_factory=list, description="Kiosk uchun tavsiya etilgan keyingi tugmalar")`
  - `session_id: str` ("Amaldagi sessiya identifikatori")
- `FAQItem`: `question: str`, `answer: str`, `category: str`
- `FAQResponse`: `items: list[FAQItem]`
- `ClearSessionResponse`: `message: str`, `session_id: str`

### 2.2 Sxemalar Eksporti (`backend/app/schemas/__init__.py`)
Yangi sxemalarni markaziy `__init__.py` ga qo'sh va eksport qil.

### 2.3 Prompts va FAQ Bilimlar Bazasi (`backend/app/services/ai_agent/prompts.py`)
- `SYSTEM_PROMPT`: Agent shaxsiyati, kutubxona qoidalari, xushmuomalalik, javob berish tili va cheklovlar.
- `FAQ_DATA`: Kamida 6-8 ta asosiy savol-javoblar (ish vaqti, a'zolik, kitob olish muddati, navbat, qoidalar, joylashuv).
- `SHELF_GUIDE`: Janrlar va ularning qavat/javon bloklari ma'lumotnomasi.
- `SUGGESTED_QUICK_ACTIONS`: Kiosk ekranida foydalanuvchiga qulay bo'lishi uchun tezkor tugmalar ro'yxati (masalan: `["Kitob qidirish", "Ish vaqti", "Dasturlash kitoblari", "Mening qoidalarim"]`).

### 2.4 Tools (`backend/app/services/ai_agent/tools.py`)
Async funksiyalar:
- `tool_search_books(db: AsyncSession, query: str | None = None, genre: str | None = None, limit: int = 5) -> list[Book]`:
  `BookRepository.search_and_filter` orqali real kitoblarni qidiradi.
- `tool_check_availability(db: AsyncSession, book_id: int) -> dict`:
  Kitobning mavjudligi (`status`), javoni (`shelf_location`) va agar band bo'lsa navbat holatini tekshiradi.
- `tool_get_recommendations(db: AsyncSession, genre: str | None = None, limit: int = 4) -> list[Book]`:
  Ommabop yoki "available" kitoblarni saralab beradi.
- `tool_library_faq(question_type: str) -> str | None`:
  FAQ ma'lumotlar bazasidan mos javobni topadi.
- `tool_get_all_genres(db: AsyncSession) -> list[str]`:
  Mavjud barcha janrlarni qaytaradi.

### 2.5 Sessiya Xotirasi (`backend/app/services/ai_agent/memory.py`)
- In-memory sessiya xotirasi klassi: `SessionMemoryManager`:
  - `add_message(session_id: str, role: str, content: str)`: Xabarni qo'shish (oxirgi 6 ta xabar: 3 ta user, 3 ta assistant saqlanadi).
  - `get_history(session_id: str) -> list[dict]`: Sessiya tarixini olish.
  - `clear_session(session_id: str)`: Sessiyani tozalash.
  - Xotira hajmini cheklash (maksimal 1000 sessiya).

### 2.6 Agent Yadro Mantiqi (`backend/app/services/ai_agent/agent.py`)
- `AIAgent` klassi:
  - `process_message(db: AsyncSession, message: str, session_id: str | None = None, user_id: int | None = None) -> ChatResponse`:
    1. `session_id` bo'lmasa, `uuid.uuid4()` bilan hosil qilish.
    2. Foydalanuvchi xabarini xotiraga qo'shish.
    3. **Intent tahlili (Pattern / Keyword Matcher):**
       - **Salomlashish:** ("salom", "assalomu alaykum", "hayrli kun", "qalaysiz") -> xushmuomala tanishuv javobi + tezkor harakatlar tugmalari (`suggested_actions`).
       - **Ish vaqti & Grafigi:** ("ish vaqti", "soat nechada", "ochiq", "yopiq", "shanba", "yakshanba", "grafik") -> `tool_library_faq("hours")` orqali aniq ish vaqti.
       - **Qoidalar & Muddat:** ("necha kun", "qoida", "a'zo bo'lish", "jarima", "muddat", "14 kun") -> `tool_library_faq("rules")` orqali aniq javob.
       - **Javon joylashuvi:** ("qayerda", "javon", "qavat", "blok", "joylashgan") -> agar kitob nomi tilga olingan bo'lsa kitob javonini aytish, bo'lmasa javonlar xaritasini tushuntirish.
       - **Janr & Tavsiya:** ("dasturlash", "badiiy", "tarix", "roman", "tavsiya", "qanday kitob bor", "top kitoblar") -> mos janrdagi kitoblarni `tool_search_books` orqali olib, tavsiyalar ro'yxatiga joylash.
       - **Aniq kitob qidiruvi:** Foydalanuvchi yozgan kalit so'z bo'yicha kitob qidirish.
    4. **Agar Gemini API integratsiyasi mumkin bo'lsa (`settings.GEMINI_API_KEY` mavjud bo'lsa):**
       - `httpx.AsyncClient` orqali Google Generative Language API ga `system_instruction`, topilgan kitoblar konteksti va tarixni uzatish.
       - Agar muvaffaqiyatli bo'lsa, LLM javob matnidan foydalanish.
       - Agar tarmoq xatosi, timeout yoki API xatoligi bo'lsa -> zudlik bilan lokal javobga o'tish (Fallback).
    5. **Offline / Fallback javob shakllantirish:**
       - Agar qidiruv bo'yicha kitob topilsa: kitoblar nomlari, mualliflari va javonlarini chiroyli formatlab, `recommended_books` ro'yxatiga qo'shish.
       - Agar hech narsa topilmasa: "Kechirasiz, '...' bo'yicha kitob topilmadi. Lekin quyidagi kitoblarni mutolaa qilishni tavsiya qilaman:" deb boshqa kitoblarni berish.
    6. Agent javobini xotiraga qo'shish va `ChatResponse` qaytarish.

### 2.7 Service Fasadi (`backend/app/services/ai_agent_service.py`)
- FastAPI endpointlari uchun qulay interfeys:
  - `async def ask_agent(...)`
  - `def get_library_faq(...)`
  - `def reset_session(...)`

### 2.8 API Endpoints (`backend/app/api/v1/agent.py`)
- `POST /api/v1/agent/chat`:
  - Request: `ChatRequest`
  - Response: `ChatResponse`
  - Tavsif: Kiosk va veb chat interfeysi uchun asosiy muloqot nuqtasi.
- `GET /api/v1/agent/faq`:
  - Response: `FAQResponse`
  - Tavsif: Kiosk ekranida foydalanuvchi darhol bosishi mumkin bo'lgan tez-tez beriladigan savollar.
- `DELETE /api/v1/agent/session/{session_id}`:
  - Response: `ClearSessionResponse`
  - Tavsif: Sessiya xotirasini tozalash (Kiosk 60 soniya tegilmasa chaqiriladi).

### 2.9 Router Integratsiyasi (`backend/app/api/v1/router.py`)
```python
from backend.app.api.v1.agent import router as agent_router

api_router.include_router(agent_router, prefix="/agent", tags=["AI Agent"])
```

---

## 🧪 BOSQICH 3: PYTEST TESTLAR TALABLARI (MAJBURIY)

`backend/tests/test_agent.py` faylida **kamida 14 ta avtomatlashtirilgan test** yoz:

1. `test_agent_greeting_uzbek`: "Salom" yoki "Assalomu alaykum" deb yozilganda, agent o'zbekcha xushmuomala tanishishi va tavsiya harakatlari (`suggested_actions`) qaytishi.
2. `test_agent_faq_library_hours`: "Kutubxona ish vaqti qachon?" deb so'ralganda, dushanba-juma 08:30-18:00 va shanba kunlari haqida to'g'ri ma'lumot berishi.
3. `test_agent_faq_borrow_rules`: "Kitob necha kunga beriladi?" deb so'ralganda, 14 kunlik muddat va 3 ta kitoblik limit haqida javob berishi.
4. `test_agent_faq_membership`: "Qanday a'zo bo'lish mumkin?" deb so'ralganda, talabalik guvohnomasi / ID karta haqida tushuntirishi.
5. `test_agent_search_books_by_genre`: "Dasturlash bo'yicha kitoblar bormi?" deb so'ralganda, bazadagi Python/IT kitoblarini tavsiya qilishi va `recommended_books` bo'sh bo'lmasligi.
6. `test_agent_search_books_by_keyword`: "O'tkan kunlar bormi?" deb so'ralganda, Abdulla Qodiriyning "O'tkan kunlar" kitobini topib berishi.
7. `test_agent_book_shelf_location_inquiry`: "O'tkan kunlar qaysi javonda?" deb so'ralganda, kitobning aniq `shelf_location` (javon) manzilini ko'rsatishi.
8. `test_agent_book_availability_status`: Kitob holati haqida so'ralganda, uning "available" (bo'sh) yoki "borrowed" (band) ekanligini to'g'ri aytishi.
9. `test_agent_nonexistent_book_fallback`: Bazada mutlaqo yo'q kitob (masalan "Kvanto mexanika 2099") so'ralganda, yo'qligini aytib, o'rniga boshqa tavsiyalarni taklif qilishi (hech qanday xato chiqmasligi).
10. `test_agent_session_memory_context`: Bir xil `session_id` bilan ketma-ket 2 ta savol berilganda, xotirada 4 ta xabar (2 user + 2 assistant) saqlanib turishi.
11. `test_agent_session_clear_api`: `DELETE /api/v1/agent/session/{session_id}` chaqirilganda, sessiya xotirasi tozalanib, muvaffaqiyatli xabar qaytishi.
12. `test_agent_chat_api_success`: `POST /api/v1/agent/chat` HTTP endpointi to'g'ri 200 status va `ChatResponse` formati qaytarishi.
13. `test_agent_chat_api_empty_message_validation`: Bo'sh matn yuborilganda 422 Unprocessable Entity xatoligi qaytishi.
14. `test_agent_faq_list_api`: `GET /api/v1/agent/faq` endpointi barcha savol-javoblar ro'yxatini qaytarishi.
15. `test_agent_offline_fallback_without_gemini_key`: `settings.GEMINI_API_KEY = ""` bo'lganda ham agent hech qanday xatosiz to'liq va mukammal ishlashi.

### Testlarni ishga tushirish:
```bash
pytest backend/tests/test_agent.py -v
pytest -v
```
**(Barcha testlar: 14 auth + 12 books + 12 search + 14 borrows + 14-15 agent = kamida 66-67 ta test 100% muvaffaqiyatli o'tishi shart!)**

---

## 📊 BOSQICH 4: HISOBOT (ISH TUGAGACH YOZILADI)

Barcha testlar muvaffaqiyatli o'tgach, `promptlar/5-agent-hisoboti.md` fayliga quyidagi formatda hisobot yoz:

```markdown
# 🤖 5-AGENT: AQLLI AI YORDAMCHI AGENTI YAKUNIY HISOBOTI

## Yozilgan / Tahrirlangan fayllar:
| Fayl | Qator soni | Holat |
|---|---|---|
| backend/app/schemas/ai.py | XX | ✅ |
| backend/app/schemas/__init__.py | XX | ✅ |
| backend/app/services/ai_agent/prompts.py | XX | ✅ |
| backend/app/services/ai_agent/tools.py | XX | ✅ |
| backend/app/services/ai_agent/memory.py | XX | ✅ |
| backend/app/services/ai_agent/agent.py | XX | ✅ |
| backend/app/services/ai_agent_service.py | XX | ✅ |
| backend/app/api/v1/agent.py | XX | ✅ |
| backend/app/api/v1/router.py | XX | ✅ |
| backend/tests/test_agent.py | XX | ✅ |
| JAMI | ~XXX | ✅ |

## Test natijalari:
[pytest natijalaridan parcha: XX passed]

## 📌 6-AGENT (KIOSK VA WEB FRONTEND — OZOD NE'MATULLAYEV) UCHUN QO'LLANMA:
- Chat endpointi: `POST /api/v1/agent/chat`
  - Body: `{"message": "Dasturlash kitoblari bormi?", "session_id": "ixtiyoriy-uuid"}`
  - Response:
    ```json
    {
      "response_text": "Kutubxonamizda dasturlash bo'yicha quyidagi ajoyib kitoblar mavjud...",
      "recommended_books": [
        {
          "id": 1,
          "title": "Python Asoslari",
          "author": "Guido van Rossum",
          "genre": "Dasturlash",
          "shelf_location": "2-qavat, A-1 javon",
          "status": "available"
        }
      ],
      "suggested_actions": ["Javon joylashuvi", "Ish vaqti", "Boshqa kitoblar"],
      "session_id": "uuid-str"
    }
    ```
- FAQ endpointi: `GET /api/v1/agent/faq` (Kiosk bosh sahifasida ko'rsatish uchun)
- Sessiyani tozalash: `DELETE /api/v1/agent/session/{session_id}` (Kiosk 60 soniya idle bo'lganda)
```

---

## 🌿 Ishchi Branch
`azimbek/ai-agent`

## ⚠️ MUHIM ESLATMALAR:
1. **Oldingi 52 ta testni aslo buzma:** 1-4 agentlar yaratgan testlarning barchasi yashil (PASSED) bo'lib qolishi shart.
2. **Hech qanday uydirma (hallyutsinatsiya) bo'lmasin:** Tavsiya qilinadigan barcha kitoblar ma'lumotlar bazasidan olinishi shart.
3. **Latency (Kechikish):** Kiosk uchun 2 soniyadan kam vaqtda javob qaytishi lozim.
4. **Offline barqarorlik:** Gemini API kaliti bo'lmaganda yoki internet yo'qligida ham agent o'z ishini to'laqonli bajara olishi shart.
