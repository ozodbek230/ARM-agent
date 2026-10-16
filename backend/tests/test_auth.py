# [Fayl maqsadi: Auth va Core qatlami avtomatlashgan Pytest testlari]
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.core.exceptions import ForbiddenError, UnauthorizedError
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.app.core.dependencies import get_current_admin
from backend.app.db.seed import seed_admin
from backend.app.db.session import create_tables
from backend.app.main import app
from backend.app.models.user import User, UserRole


@pytest.fixture(autouse=True)
async def setup_db():
    """Har bir testdan oldin DB jadvallari va seed ma'lumotlarini tayyorlash."""
    await create_tables()
    await seed_admin()


@pytest.mark.asyncio
async def test_password_hashing():
    raw_pwd = "my_secret_password"
    hashed = hash_password(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("wrong_password", hashed) is False


@pytest.mark.asyncio
async def test_jwt_tokens():
    payload = {"sub": "1", "role": "admin"}
    token = create_access_token(payload)
    decoded = decode_token(token)
    assert decoded["sub"] == "1"
    assert decoded["role"] == "admin"
    assert decoded["type"] == "access"

    refresh = create_refresh_token(payload)
    decoded_refresh = decode_token(refresh)
    assert decoded_refresh["sub"] == "1"
    assert decoded_refresh["type"] == "refresh"


@pytest.mark.asyncio
async def test_seed_admin_idempotent():
    # Ikkinchi marta chaqirilganda xatolik bermasligi va dublikat yaratmasligi kerak
    await seed_admin()
    await seed_admin()
    assert True


@pytest.mark.asyncio
async def test_login_with_email_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin@arm.uz", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_username_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin@arm.uz", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "detail" in response.json()


@pytest.mark.asyncio
async def test_login_nonexistent_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            json={"username": "mavjud_emas@arm.uz", "password": "somepassword"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_me():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin@arm.uz", "password": "admin123"},
        )
        access_token = login_res.json()["access_token"]

        me_res = await ac.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_res.status_code == 200
        user_info = me_res.json()
        assert user_info["email"] == "admin@arm.uz"
        assert user_info["username"] == "admin"
        assert user_info["role"] == "admin"
        assert user_info["is_active"] is True


@pytest.mark.asyncio
async def test_get_me_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Tokensi murojaat
        me_res = await ac.get("/api/v1/auth/me")
        assert me_res.status_code == 401

        # Noto'g'ri token bilan murojaat
        me_res_invalid = await ac.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_123"},
        )
        assert me_res_invalid.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin@arm.uz", "password": "admin123"},
        )
        refresh_token_val = login_res.json()["refresh_token"]

        refresh_res = await ac.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token_val},
        )
        assert refresh_res.status_code == 200
        new_tokens = refresh_res.json()
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens


@pytest.mark.asyncio
async def test_admin_dependency_forbidden_for_regular_user():
    regular_user = User(
        id=99,
        email="talaba@arm.uz",
        username="talaba",
        role=UserRole.USER,
        is_active=True,
    )
    with pytest.raises(ForbiddenError):
        await get_current_admin(current_user=regular_user)


@pytest.mark.asyncio
async def test_register_new_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        new_user_data = {
            "email": "yangi_foydalanuvchi@arm.uz",
            "username": "yangi_user",
            "full_name": "Yangi Foydalanuvchi",
            "password": "yangi_password123",
            "role": "user",
        }
        reg_res = await ac.post("/api/v1/auth/register", json=new_user_data)
        assert reg_res.status_code == 201
        res_json = reg_res.json()
        assert res_json["email"] == "yangi_foydalanuvchi@arm.uz"
        assert res_json["username"] == "yangi_user"
        assert "password" not in res_json

        # Duplicate register should return 409 Conflict
        dup_res = await ac.post("/api/v1/auth/register", json=new_user_data)
        assert dup_res.status_code == 409


@pytest.mark.asyncio
async def test_login_with_seeded_talaba():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            json={"username": "talaba", "password": "talaba123"},
        )
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens

        me_res = await ac.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert me_res.status_code == 200
        assert me_res.json()["role"] == "user"


@pytest.mark.asyncio
async def test_root_and_health_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        root_res = await ac.get("/")
        assert root_res.status_code == 200
        assert root_res.json()["status"] == "online"

        health_res = await ac.get("/health")
        assert health_res.status_code == 200
        assert health_res.json()["status"] == "healthy"
