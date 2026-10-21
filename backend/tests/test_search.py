# [Fayl maqsadi: Qidiruv va filtrlash domeni avtomatlashgan Pytest testlari (3-agent)]
import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.core.security import hash_password
from backend.app.db.seed import seed_admin, seed_books
from backend.app.db.session import AsyncSessionLocal, create_tables
from backend.app.main import app


@pytest.fixture(autouse=True)
async def setup_db():
    """Har bir testdan oldin DB jadvallari va seed ma'lumotlarini tayyorlash."""
    await create_tables()
    await seed_admin()
    await seed_books()


# ---------------------------------------------------------------------------
# 1. Kitob nomining qismi bo'yicha qidirish
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_by_title_partial():
    """Kitob nomining bir qismi bilan qidirish natija qaytarishi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/books/search", params={"query": "kunlar"})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "ask_ai" in data
        assert "suggestions" in data
        # "O'tkan kunlar" seed kitobida mavjud bo'lishi kerak
        assert data["total"] >= 1
        titles = [item["title"].lower() for item in data["items"]]
        assert any("kunlar" in t for t in titles)


# ---------------------------------------------------------------------------
# 2. Katta-kichik harf farq qilmasligi (case-insensitive)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_case_insensitive():
    """Katta va kichik harflar bilan bir xil natija qaytishi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lower_res = await ac.get("/api/v1/books/search", params={"query": "o'tkan"})
        upper_res = await ac.get("/api/v1/books/search", params={"query": "O'TKAN"})

        assert lower_res.status_code == 200
        assert upper_res.status_code == 200

        lower_data = lower_res.json()
        upper_data = upper_res.json()

        assert lower_data["total"] == upper_data["total"]
        assert lower_data["total"] >= 1


# ---------------------------------------------------------------------------
# 3. Muallif ismi bo'yicha qidirish
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_by_author():
    """Muallif ismi bo'yicha qidirish natija qaytarishi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/books/search", params={"query": "Qodiriy"})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        authors = [item["author"].lower() for item in data["items"]]
        assert any("qodiriy" in a for a in authors)


# ---------------------------------------------------------------------------
# 4. Janr bo'yicha filtrlash
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_filter_by_genre():
    """Janr bo'yicha filtrlash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Avval mavjud janrlar ro'yxatini olamiz
        genres_res = await ac.get("/api/v1/books/genres")
        assert genres_res.status_code == 200
        genres = genres_res.json()
        assert len(genres) > 0

        # Birinchi janr bo'yicha filtrlash
        first_genre = genres[0]
        response = await ac.get("/api/v1/books/search", params={"genre": first_genre})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        for item in data["items"]:
            assert first_genre.lower() in item["genre"].lower()


# ---------------------------------------------------------------------------
# 5. Yil oralig'i bo'yicha filtrlash
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_filter_by_year_range():
    """Nashr yili oralig'i bo'yicha filtrlash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/books/search",
            params={"year_from": 1990, "year_to": 2025},
        )
        assert response.status_code == 200
        data = response.json()
        # Yil filtr ishlayotganini tekshirish
        for item in data["items"]:
            assert 1990 <= item["year"] <= 2025


# ---------------------------------------------------------------------------
# 6. Holat bo'yicha filtrlash
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_filter_by_status():
    """Kitob holati (status) bo'yicha filtrlash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/books/search",
            params={"status": "available"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        for item in data["items"]:
            assert item["status"] == "available"


# ---------------------------------------------------------------------------
# 7. Kombinatsiyalangan qidiruv (bir nechta parametr)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_combined_search_and_filter():
    """Bir vaqtda bir nechta parametrlar bilan filtrlash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Avval mavjud janrni bilib olamiz
        genres_res = await ac.get("/api/v1/books/genres")
        genres = genres_res.json()

        response = await ac.get(
            "/api/v1/books/search",
            params={
                "year_from": 1800,
                "year_to": 2025,
                "status": "available",
                "limit": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["limit"] == 5
        # Har bir natija ko'rsatilgan shartlarga javob berishi kerak
        for item in data["items"]:
            assert 1800 <= item["year"] <= 2025
            assert item["status"] == "available"


# ---------------------------------------------------------------------------
# 8. Saralash (asc va desc)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_sorting_asc_desc():
    """sort_by='year' parametri bilan asc va desc saralash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        asc_res = await ac.get(
            "/api/v1/books/search",
            params={"sort_by": "year", "order": "asc", "limit": 100},
        )
        desc_res = await ac.get(
            "/api/v1/books/search",
            params={"sort_by": "year", "order": "desc", "limit": 100},
        )

        assert asc_res.status_code == 200
        assert desc_res.status_code == 200

        asc_items = asc_res.json()["items"]
        desc_items = desc_res.json()["items"]

        if len(asc_items) >= 2:
            # O'sib boruvchi tartibda: birinchi yil <= oxirgi yil
            assert asc_items[0]["year"] <= asc_items[-1]["year"]

        if len(desc_items) >= 2:
            # Kamayib boruvchi tartibda: birinchi yil >= oxirgi yil
            assert desc_items[0]["year"] >= desc_items[-1]["year"]


# ---------------------------------------------------------------------------
# 9. Noto'g'ri sort_by qiymatida xato bermasdan ishlash (fallback)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_invalid_sort_fallback():
    """Noto'g'ri sort_by qiymatida server xato bermay, xavfsiz fallback bilan ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/books/search",
            params={"sort_by": "not_real_column", "order": "asc"},
        )
        # 500 yoki 422 qaytmasligi kerak
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


# ---------------------------------------------------------------------------
# 10. Pagination (skip va limit)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_pagination():
    """Qidiruv natijalarini skip va limit bilan sahifalash to'g'ri ishlashi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        page1_res = await ac.get(
            "/api/v1/books/search",
            params={"skip": 0, "limit": 2},
        )
        page2_res = await ac.get(
            "/api/v1/books/search",
            params={"skip": 2, "limit": 2},
        )

        assert page1_res.status_code == 200
        assert page2_res.status_code == 200

        page1_data = page1_res.json()
        page2_data = page2_res.json()

        assert page1_data["skip"] == 0
        assert page1_data["limit"] == 2
        assert page2_data["skip"] == 2
        assert page2_data["limit"] == 2

        if len(page1_data["items"]) > 0 and len(page2_data["items"]) > 0:
            page1_ids = {item["id"] for item in page1_data["items"]}
            page2_ids = {item["id"] for item in page2_data["items"]}
            # Ikkala sahifadagi kitoblar ID lari bir-biridan farq qilishi kerak
            assert page1_ids.isdisjoint(page2_ids)


# ---------------------------------------------------------------------------
# 11. Topilmagan qidiruv — ask_ai va suggestions qaytishi
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_search_no_results_triggers_ask_ai():
    """Qidiruvda natija topilmasa ask_ai=True va suggestions ro'yxati qaytishi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/books/search",
            params={"query": "bu_kitob_hech_qachon_mavjud_emas_xyzabc123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["ask_ai"] is True
        assert isinstance(data["suggestions"], list)


# ---------------------------------------------------------------------------
# 12. Janrlar endpointi
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_genres_endpoint():
    """GET /api/v1/books/genres unikal janrlar ro'yxatini to'g'ri qaytarishi kerak."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/books/genres")
        assert response.status_code == 200
        genres = response.json()
        assert isinstance(genres, list)
        assert len(genres) >= 1
        # Barcha qiymatlar satr bo'lishi kerak
        for genre in genres:
            assert isinstance(genre, str)
            assert len(genre) > 0
        # Takrorlanuvchi qiymatlar bo'lmasligi kerak
        assert len(genres) == len(set(genres))
