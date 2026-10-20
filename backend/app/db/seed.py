# [Fayl maqsadi: Boshlang'ich tizim ma'lumotlarini bazaga kiritish (seed data)]
from sqlalchemy import func, or_, select
from backend.app.core.security import hash_password
from backend.app.db.session import AsyncSessionLocal
from backend.app.models.book import Book, BookStatus
from backend.app.models.user import User, UserRole


async def seed_admin() -> None:
    """Tizim birinchi marta ishga tushganda admin va test foydalanuvchini idempotent tarzda yaratish."""
    async with AsyncSessionLocal() as session:
        # 1. Admin tekshirish va yaratish
        admin_query = select(User).where(
            or_(User.email == "admin@arm.uz", User.username == "admin")
        )
        admin_result = await session.execute(admin_query)
        existing_admin = admin_result.scalar_one_or_none()

        if existing_admin is None:
            admin = User(
                email="admin@arm.uz",
                username="admin",
                full_name="Bosh Administrator",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            session.add(admin)

        # 2. Test talaba tekshirish va yaratish
        user_query = select(User).where(
            or_(User.email == "talaba@arm.uz", User.username == "talaba")
        )
        user_result = await session.execute(user_query)
        existing_user = user_result.scalar_one_or_none()

        if existing_user is None:
            student = User(
                email="talaba@arm.uz",
                username="talaba",
                full_name="Test Talaba",
                hashed_password=hash_password("talaba123"),
                role=UserRole.USER,
                is_active=True,
            )
            session.add(student)

        await session.commit()


async def seed_books() -> None:
    """Tizim birinchi marta ishga tushganda boshlang'ich kitoblar to'plamini idempotent tarzda kiritish."""
    async with AsyncSessionLocal() as session:
        count_res = await session.execute(select(func.count()).select_from(Book))
        total_books = count_res.scalar() or 0
        if total_books > 0:
            return

        initial_books = [
            Book(
                title="O'tkan kunlar",
                author="Abdulla Qodiriy",
                genre="Tarixiy roman",
                year=1925,
                shelf_location="1-qavat, B-2 javon",
                status=BookStatus.AVAILABLE.value,
                description="O'zbek adabiyotidagi birinchi roman bo'lib, Turkiston xonliklari davridagi ijtimoiy ziddiyatlar va sof muhabbatni tasvirlaydi.",
            ),
            Book(
                title="Mehrobdan chayon",
                author="Abdulla Qodiriy",
                genre="Tarixiy roman",
                year=1928,
                shelf_location="1-qavat, B-2 javon",
                status=BookStatus.AVAILABLE.value,
                description="XIX asr Xudoyorxon davridagi saroy fitnalari, adolatsizliklar va oddiy xalq hayotiga bag'ishlangan tarixiy asar.",
            ),
            Book(
                title="Clean Code",
                author="Robert C. Martin",
                genre="Dasturlash",
                year=2008,
                shelf_location="2-qavat, IT-1 javon",
                status=BookStatus.AVAILABLE.value,
                description="Dasturchilar uchun toza va sifatli kod yozish qoidalari, refactoring va dasturiy arxitektura bo'yicha qo'llanma.",
            ),
            Book(
                title="Python Crash Course",
                author="Eric Matthes",
                genre="Dasturlash",
                year=2019,
                shelf_location="2-qavat, IT-1 javon",
                status=BookStatus.AVAILABLE.value,
                description="Python dasturlash tilini noldan boshlab loyihalar orqali o'rganish bo'yicha eng mashhur amaliy qo'llanma.",
            ),
            Book(
                title="Atomic Habits",
                author="James Clear",
                genre="Shaxsiy rivojlanish",
                year=2018,
                shelf_location="3-qavat, SR-4 javon",
                status=BookStatus.AVAILABLE.value,
                description="Kichik odatlarning ulkan o'zgarishlarga olib kelishi hamda samarasiz odatlardan qutulish usullari.",
            ),
            Book(
                title="Yulduzli tunlar",
                author="Pirimqul Qodirov",
                genre="Tarixiy roman",
                year=1978,
                shelf_location="1-qavat, B-3 javon",
                status=BookStatus.AVAILABLE.value,
                description="Zahiriddin Muhammad Boburning murakkab hayot yo'li va Boburiylar saltanatining vujudga kelishi haqidagi epik asar.",
            ),
            Book(
                title="Shum bola",
                author="G'afur G'ulom",
                genre="Badiiy adabiyot",
                year=1936,
                shelf_location="1-qavat, B-1 javon",
                status=BookStatus.AVAILABLE.value,
                description="Inqilobdan oldingi Toshkent hayoti va zukko Shum bolaning sarguzashtlari haqidagi qissa.",
            ),
            Book(
                title="The Pragmatic Programmer",
                author="David Thomas, Andrew Hunt",
                genre="Dasturlash",
                year=2019,
                shelf_location="2-qavat, IT-2 javon",
                status=BookStatus.AVAILABLE.value,
                description="Dasturiy injiniringda professionalizm, arxitektura va amaliy mahoratga erishish yo'llari.",
            ),
            Book(
                title="Sariq devni minib",
                author="Xudoyberdi To'xtaboyev",
                genre="Sarguzasht",
                year=1968,
                shelf_location="1-qavat, B-1 javon",
                status=BookStatus.AVAILABLE.value,
                description="Sehrli shlyapa egasi Hoshimjonning kulgili va ibratli sarguzashtlari haqidagi mashhur asar.",
            ),
            Book(
                title="Deep Work",
                author="Cal Newport",
                genre="Shaxsiy rivojlanish",
                year=2016,
                shelf_location="3-qavat, SR-2 javon",
                status=BookStatus.AVAILABLE.value,
                description="Chalg'ituvchi omillarga to'la dunyoda diqqatni chuqur jamlash va yuqori samaradorlikka erishish qoidalari.",
            ),
        ]
        session.add_all(initial_books)
        await session.commit()
