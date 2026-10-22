# [Fayl maqsadi: Ijara va Bron domeni avtomatlashgan Pytest testlari]
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from backend.app.core.security import hash_password
from backend.app.db.seed import seed_admin, seed_books
from backend.app.db.session import AsyncSessionLocal, create_tables
from backend.app.main import app
from backend.app.models.book import Book
from backend.app.models.user import User


@pytest.fixture(autouse=True)
async def setup_db():
    """Har bir testdan oldin DB jadvallari va seed ma'lumotlarini tayyorlash.
    Testdan keyin borrows, reservations tozalanadi va kitoblar 'available' ga qaytariladi.
    """
    await create_tables()
    await seed_admin()
    await seed_books()

    yield  # Test ishlaydi

    # ─── TEARDOWN ─────────────────────────────────────────────────────────────
    from sqlalchemy import delete, update as sa_update
    from backend.app.models.borrow import Borrow, Reservation
    from backend.app.models.book import Book
    from backend.app.models.user import User as UserModel

    async with AsyncSessionLocal() as session:
        # Bronlarni o'chirish
        await session.execute(delete(Reservation))
        # Ijaralarni o'chirish
        await session.execute(delete(Borrow))
        # Barcha kitoblar statusini "available" ga qaytarish
        await session.execute(
            sa_update(Book).values(status="available")
        )
        # Qo'shimcha foydalanuvchilarni o'chirish (admin va talaba qolsin)
        await session.execute(
            delete(UserModel).where(
                UserModel.username.not_in(["admin", "talaba"])
            )
        )
        await session.commit()


# ─── YORDAMCHI FUNKSIYALAR ────────────────────────────────────────────────────

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


async def create_extra_user(username: str, email: str, password: str = "pass123") -> str:
    """Yangi foydalanuvchi yaratib, uning tokenini qaytaradi."""
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.username == username))
        user = res.scalar_one_or_none()
        if not user:
            user = User(
                email=email,
                username=username,
                full_name=username,
                hashed_password=hash_password(password),
                role="user",
                is_active=True,
            )
            session.add(user)
            await session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": email, "password": password},
        )
        return login_res.json()["access_token"]


async def get_first_available_book_id() -> int:
    """Bazadan birinchi 'available' kitob ID sini olish."""
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Book).where(Book.status == "available").limit(1))
        book = res.scalar_one_or_none()
        if not book:
            # Agar available kitob bo'lmasa, barcha kitoblardan birinchisini "available" qilib olish
            res2 = await session.execute(select(Book).limit(1))
            book = res2.scalar_one_or_none()
            if book:
                book.status = "available"
                await session.commit()
        return book.id if book else 1


async def force_book_status(book_id: int, status: str) -> None:
    """Kitob holatini majburan o'zgartirish (test yordamchisi)."""
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Book).where(Book.id == book_id))
        book = res.scalar_one_or_none()
        if book:
            book.status = status
            await session.commit()


# ─── TESTLAR ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_borrow_available_book_success():
    """1. Bo'sh kitobni ijaraga olish va kitob statusi 'borrowed' ga aylanishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id, "days": 14},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["book_id"] == book_id
        assert data["status"] == "active"
        assert data["returned_date"] is None

    # Kitob statusi o'zgardi?
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Book).where(Book.id == book_id))
        book = res.scalar_one_or_none()
        assert book is not None
        assert book.status == "borrowed"


@pytest.mark.asyncio
async def test_borrow_already_borrowed_book_fails():
    """2. Band kitobni olishga urinishda 400 xatolik chiqishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Birinchi ijara
        r1 = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert r1.status_code == 201

        # Ikkinchi urinish
        r2 = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert r2.status_code == 400
        assert "band" in r2.json()["detail"]


@pytest.mark.asyncio
async def test_borrow_nonexistent_book_fails():
    """3. Mavjud bo'lmagan kitobda 404 chiqishi."""
    _, student_token = await get_auth_tokens()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/borrows",
            json={"book_id": 999999},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_borrow_unauthorized_fails():
    """4. Tokensiz so'rovda 401 chiqishi."""
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_return_book_success():
    """5. Kitob qaytarilganda uning holati 'available' ga aylanishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        borrow_res = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert borrow_res.status_code == 201
        borrow_id = borrow_res.json()["id"]

        return_res = await ac.post(
            "/api/v1/borrows/return",
            json={"borrow_id": borrow_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert return_res.status_code == 200
        data = return_res.json()
        assert data["status"] == "returned"
        assert data["returned_date"] is not None

    # Kitob statusi qaytdi?
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Book).where(Book.id == book_id))
        book = res.scalar_one_or_none()
        assert book.status == "available"


@pytest.mark.asyncio
async def test_return_already_returned_book_fails():
    """6. Qaytarilgan kitobni qayta qaytarishda 400 chiqishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        borrow_res = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        borrow_id = borrow_res.json()["id"]

        # Birinchi qaytarish
        await ac.post(
            "/api/v1/borrows/return",
            json={"borrow_id": borrow_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )

        # Ikkinchi qaytarish urinishi
        r2 = await ac.post(
            "/api/v1/borrows/return",
            json={"borrow_id": borrow_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert r2.status_code == 400
        assert "qaytarilgan" in r2.json()["detail"]


@pytest.mark.asyncio
async def test_return_other_users_book_forbidden():
    """7. Boshqa birovning kitobini qaytarishga urinishda 403 chiqishi."""
    _, student_token = await get_auth_tokens()
    other_token = await create_extra_user("other_student", "other@arm.uz")
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # student kitob oladi
        borrow_res = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert borrow_res.status_code == 201
        borrow_id = borrow_res.json()["id"]

        # other_student qaytarishga urinadi
        r = await ac.post(
            "/api/v1/borrows/return",
            json={"borrow_id": borrow_id},
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert r.status_code == 403


@pytest.mark.asyncio
async def test_get_my_borrows():
    """8. Foydalanuvchi faqat o'ziga tegishli kitoblarni ko'rishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )

        response = await ac.get(
            "/api/v1/borrows/my",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1
        assert any(item["book_id"] == book_id for item in data["items"])


@pytest.mark.asyncio
async def test_reserve_borrowed_book_success():
    """9. Band kitobga navbatga yozilish (queue_position = 1)."""
    admin_token, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Admin kitob oladi
        await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Student navbatga yoziladi
        res = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert res.status_code == 201
        data = res.json()
        assert data["book_id"] == book_id
        assert data["queue_position"] == 1
        assert data["status"] == "waiting"


@pytest.mark.asyncio
async def test_reserve_available_book_fails():
    """10. Bo'sh turgan kitobni bron qilishga urinishda 400 chiqishi."""
    _, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 400
        assert "bo'sh" in response.json()["detail"]


@pytest.mark.asyncio
async def test_duplicate_reservation_fails():
    """11. Bir kitobga ayni foydalanuvchi qayta navbatga yozila olmasligi."""
    admin_token, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        r1 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert r1.status_code == 201

        r2 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert r2.status_code == 400
        assert "allaqachon" in r2.json()["detail"]


@pytest.mark.asyncio
async def test_reservation_queue_max_limit():
    """12. 4-odam navbatga yozilmoqchi bo'lsa navbat to'lgan deb 400 qaytishi."""
    admin_token, _ = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    # 3 ta qo'shimcha foydalanuvchi yaratish
    tok1 = await create_extra_user("q_user1", "quser1@arm.uz")
    tok2 = await create_extra_user("q_user2", "quser2@arm.uz")
    tok3 = await create_extra_user("q_user3", "quser3@arm.uz")
    tok4 = await create_extra_user("q_user4", "quser4@arm.uz")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Admin kitob oladi
        await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # 3 ta navbat to'ldirish
        for tok in [tok1, tok2, tok3]:
            r = await ac.post(
                "/api/v1/borrows/reservations",
                json={"book_id": book_id},
                headers={"Authorization": f"Bearer {tok}"},
            )
            assert r.status_code == 201

        # 4-odam urinishi
        r4 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {tok4}"},
        )
        assert r4.status_code == 400
        assert "to'lgan" in r4.json()["detail"]


@pytest.mark.asyncio
async def test_return_book_notifies_first_in_queue():
    """13. Kitob qaytarilganda 1-o'rindagi bron 'notified' va kitob 'reserved' bo'lishi."""
    admin_token, student_token = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Admin kitob oladi
        borrow_res = await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert borrow_res.status_code == 201
        borrow_id = borrow_res.json()["id"]

        # Student navbatga yoziladi
        res_res = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert res_res.status_code == 201
        reservation_id = res_res.json()["id"]

        # Admin kitobni qaytaradi
        return_res = await ac.post(
            "/api/v1/borrows/return",
            json={"borrow_id": borrow_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert return_res.status_code == 200

    # Bron "notified" ga o'tgani va kitob "reserved" ligini tekshirish
    from backend.app.models.borrow import Reservation
    async with AsyncSessionLocal() as session:
        res = await session.execute(
            select(Reservation).where(Reservation.id == reservation_id)
        )
        reservation = res.scalar_one_or_none()
        assert reservation is not None
        assert reservation.status == "notified"

        book_res = await session.execute(select(Book).where(Book.id == book_id))
        book = book_res.scalar_one_or_none()
        assert book.status == "reserved"


@pytest.mark.asyncio
async def test_cancel_reservation_shifts_queue():
    """14. Bron bekor qilinganda qolganlarning o'rni oldinga siljishi."""
    admin_token, _ = await get_auth_tokens()
    book_id = await get_first_available_book_id()

    tok1 = await create_extra_user("shift_user1", "shift1@arm.uz")
    tok2 = await create_extra_user("shift_user2", "shift2@arm.uz")
    tok3 = await create_extra_user("shift_user3", "shift3@arm.uz")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Admin kitob oladi
        await ac.post(
            "/api/v1/borrows",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # 3 ta navbat
        r1 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {tok1}"},
        )
        assert r1.status_code == 201
        res1_id = r1.json()["id"]

        r2 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {tok2}"},
        )
        assert r2.status_code == 201
        res2_id = r2.json()["id"]

        r3 = await ac.post(
            "/api/v1/borrows/reservations",
            json={"book_id": book_id},
            headers={"Authorization": f"Bearer {tok3}"},
        )
        assert r3.status_code == 201
        res3_id = r3.json()["id"]

        # 1-o'rindagi (tok1) bronni bekor qilish
        cancel_res = await ac.delete(
            f"/api/v1/borrows/reservations/{res1_id}",
            headers={"Authorization": f"Bearer {tok1}"},
        )
        assert cancel_res.status_code == 200

    # Bekor qilingandan keyin 2-odam 1-o'ringa, 3-odam 2-o'ringa o'tgani tekshiriladi
    from backend.app.models.borrow import Reservation
    async with AsyncSessionLocal() as session:
        res_r1 = await session.execute(select(Reservation).where(Reservation.id == res1_id))
        r1_obj = res_r1.scalar_one_or_none()
        assert r1_obj.status == "cancelled"

        res_r2 = await session.execute(select(Reservation).where(Reservation.id == res2_id))
        r2_obj = res_r2.scalar_one_or_none()
        assert r2_obj.queue_position == 1

        res_r3 = await session.execute(select(Reservation).where(Reservation.id == res3_id))
        r3_obj = res_r3.scalar_one_or_none()
        assert r3_obj.queue_position == 2
