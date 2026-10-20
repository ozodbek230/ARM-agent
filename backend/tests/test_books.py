# [Fayl maqsadi: Kitoblar domeni (Books Core) avtomatlashgan Pytest testlari]
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from backend.app.core.security import hash_password
from backend.app.db.seed import seed_admin, seed_books
from backend.app.db.session import AsyncSessionLocal, create_tables
from backend.app.main import app
from backend.app.models.user import User


@pytest.fixture(autouse=True)
async def setup_db():
    """Har bir testdan oldin DB jadvallari va seed ma'lumotlarini tayyorlash."""
    await create_tables()
    await seed_admin()
    await seed_books()


async def get_auth_tokens():
    """Admin va talaba foydalanuvchilari uchun access tokenlarni olish."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin@arm.uz", "password": "admin123"},
        )
        admin_token = admin_res.json()["access_token"]

        student_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "talaba", "password": "talaba123"},
        )
        student_token = student_res.json()["access_token"]

        return admin_token, student_token


async def get_librarian_token():
    """Kutubxonachi (Librarian) roli uchun foydalanuvchi yaratish va token olish."""
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.username == "librarian_test"))
        librarian = res.scalar_one_or_none()
        if not librarian:
            librarian = User(
                email="librarian_test@arm.uz",
                username="librarian_test",
                full_name="Test Kutubxonachi",
                hashed_password=hash_password("lib123"),
                role="librarian",
                is_active=True,
            )
            session.add(librarian)
            await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "librarian_test@arm.uz", "password": "lib123"},
        )
        return login_res.json()["access_token"]


@pytest.mark.asyncio
async def test_get_books_empty_or_seeded():
    """1. Kitoblar ro'yxatini pagination va jami soni bilan olish testi."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/books")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        assert isinstance(data["items"], list)
        assert data["total"] >= len(data["items"])
        assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_book_by_id_success():
    """2. Mavjud kitobni ID bo'yicha olish testi."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        list_res = await ac.get("/api/v1/books")
        assert list_res.status_code == 200
        first_book_id = list_res.json()["items"][0]["id"]

        detail_res = await ac.get(f"/api/v1/books/{first_book_id}")
        assert detail_res.status_code == 200
        book = detail_res.json()
        assert book["id"] == first_book_id
        assert "title" in book
        assert "author" in book
        assert "genre" in book
        assert "shelf_location" in book
        assert "status" in book


@pytest.mark.asyncio
async def test_get_book_not_found():
    """3. Mavjud bo'lmagan ID bo'yicha kitob so'ralganda 404 qaytishi testi."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/books/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Kitob topilmadi"


@pytest.mark.asyncio
async def test_create_book_as_admin_success():
    """4. Administrator yangi kitob yarata olishi testi."""
    admin_token, _ = await get_auth_tokens()
    new_book_data = {
        "title": "Sun'iy Intellekt Asoslari",
        "author": "Stuart Russell, Peter Norvig",
        "genre": "Sun'iy Intellekt",
        "year": 2020,
        "shelf_location": "2-qavat, AI-1 javon",
        "status": "available",
        "description": "Zamonaviy sun'iy intellekt nazariyasi va amaliyoti.",
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/books",
            json=new_book_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        created = response.json()
        assert created["title"] == new_book_data["title"]
        assert created["author"] == new_book_data["author"]
        assert created["shelf_location"] == new_book_data["shelf_location"]
        assert "id" in created
        assert "created_at" in created


@pytest.mark.asyncio
async def test_create_book_as_unauthorized_fails():
    """5. Tokensiz murojaat qilinganda 401 Unauthorized qaytishi testi."""
    book_payload = {
        "title": "Avtorizatsiyasiz Kitob",
        "author": "Noma'lum",
        "genre": "Badiiy",
        "year": 2022,
        "shelf_location": "1-qavat",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/books", json=book_payload)
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_book_as_student_forbidden():
    """6. Oddiy talaba yangi kitob qo'shishga uringanda 403 Forbidden qaytishi testi."""
    _, student_token = await get_auth_tokens()
    book_payload = {
        "title": "Talaba Kitobi",
        "author": "Test Muallif",
        "genre": "Badiiy",
        "year": 2024,
        "shelf_location": "1-qavat, T-1 javon",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/books",
            json=book_payload,
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_book_success():
    """7. Admin tomonidan kitob ma'lumotlarini qisman va to'liq yangilash testi."""
    admin_token, _ = await get_auth_tokens()

    # Dastlab bitta kitob yaratamiz
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_res = await ac.post(
            "/api/v1/books",
            json={
                "title": "Yangilanishdan oldingi nom",
                "author": "Dastlabki Muallif",
                "genre": "Ilmiy",
                "year": 2020,
                "shelf_location": "1-qavat, B-5 javon",
                "status": "available",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_res.status_code == 201
        book_id = create_res.json()["id"]

        # Kitob nomini va javonini o'zgartiramiz
        update_res = await ac.put(
            f"/api/v1/books/{book_id}",
            json={
                "title": "Yangilangan Kitob Nomi",
                "shelf_location": "2-qavat, B-10 javon",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert update_res.status_code == 200
        updated = update_res.json()
        assert updated["id"] == book_id
        assert updated["title"] == "Yangilangan Kitob Nomi"
        assert updated["shelf_location"] == "2-qavat, B-10 javon"
        # O'zgartirilmagan maydonlar asl holida qolganini tekshiramiz
        assert updated["author"] == "Dastlabki Muallif"
        assert updated["genre"] == "Ilmiy"


@pytest.mark.asyncio
async def test_update_book_not_found():
    """8. Mavjud bo'lmagan kitobni yangilashga uringanda 404 qaytishi testi."""
    admin_token, _ = await get_auth_tokens()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put(
            "/api/v1/books/999999",
            json={"title": "Hech qachon mavjud bo'lmagan kitob"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Kitob topilmadi"


@pytest.mark.asyncio
async def test_delete_book_as_admin_success():
    """9. Administrator kitobni muvaffaqiyatli o'chira olishi testi."""
    admin_token, _ = await get_auth_tokens()

    # O'chirish uchun yangi kitob yaratamiz
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_res = await ac.post(
            "/api/v1/books",
            json={
                "title": "O'chirilishi kerak bo'lgan kitob",
                "author": "Vaqtinchalik Muallif",
                "genre": "Test",
                "year": 2023,
                "shelf_location": "0-qavat, Omborda",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_res.status_code == 201
        book_id = create_res.json()["id"]

        # O'chiramiz
        del_res = await ac.delete(
            f"/api/v1/books/{book_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert del_res.status_code == 200
        assert del_res.json()["message"] == "Kitob muvaffaqiyatli o'chirildi"

        # Qayta so'ralganda 404 berishi kerak
        get_res = await ac.get(f"/api/v1/books/{book_id}")
        assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_delete_book_as_student_forbidden():
    """10. Oddiy talaba kitobni o'chirishga uringanda 403 Forbidden qaytishi testi."""
    admin_token, student_token = await get_auth_tokens()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        list_res = await ac.get("/api/v1/books")
        first_book_id = list_res.json()["items"][0]["id"]

        del_res = await ac.delete(
            f"/api/v1/books/{first_book_id}",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert del_res.status_code == 403


@pytest.mark.asyncio
async def test_create_and_update_book_as_librarian():
    """11. Kutubxonachi (Librarian) roli kitob qo'shish va yangilay olishi testi."""
    librarian_token = await get_librarian_token()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Kutubxonachi yangi kitob qo'shadi
        create_res = await ac.post(
            "/api/v1/books",
            json={
                "title": "Kutubxonachi Kiritgan Kitob",
                "author": "Muallif X",
                "genre": "Ma'lumotnoma",
                "year": 2024,
                "shelf_location": "2-qavat, K-1 javon",
            },
            headers={"Authorization": f"Bearer {librarian_token}"},
        )
        assert create_res.status_code == 201
        book_id = create_res.json()["id"]

        # Kutubxonachi kitobni tahrirlaydi
        update_res = await ac.put(
            f"/api/v1/books/{book_id}",
            json={"title": "Kutubxonachi Kiritgan Kitob (Tahrirlangan)"},
            headers={"Authorization": f"Bearer {librarian_token}"},
        )
        assert update_res.status_code == 200
        assert update_res.json()["title"] == "Kutubxonachi Kiritgan Kitob (Tahrirlangan)"

        # Ammo kutubxonachi kitobni o'chira olmasligi kerak (DELETE faqat admin uchun)
        del_res = await ac.delete(
            f"/api/v1/books/{book_id}",
            headers={"Authorization": f"Bearer {librarian_token}"},
        )
        assert del_res.status_code == 403


@pytest.mark.asyncio
async def test_books_pagination_parameters():
    """12. Pagination parametrlari (skip, limit) to'g'ri ishlashi testi."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_limit_2 = await ac.get("/api/v1/books?skip=0&limit=2")
        assert res_limit_2.status_code == 200
        data_2 = res_limit_2.json()
        assert len(data_2["items"]) == 2
        assert data_2["skip"] == 0
        assert data_2["limit"] == 2

        res_skip_2 = await ac.get("/api/v1/books?skip=2&limit=2")
        assert res_skip_2.status_code == 200
        data_skip = res_skip_2.json()
        assert len(data_skip["items"]) <= 2
        assert data_skip["skip"] == 2
        # Birinchi sahifadagi kitoblar ikkinchi sahifadagilardan farq qilishi kerak
        if len(data_skip["items"]) > 0:
            assert data_2["items"][0]["id"] != data_skip["items"][0]["id"]
