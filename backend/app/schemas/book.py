# [Fayl maqsadi: Kitob (Book) ma'lumotlari uchun Pydantic v2 sxemalari]
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Kitob nomi")
    author: str = Field(..., min_length=1, max_length=255, description="Kitob muallifi")
    genre: str = Field(..., min_length=1, max_length=100, description="Kitob janri")
    year: int = Field(..., ge=0, le=2100, description="Nashr etilgan yili")
    shelf_location: str = Field(..., min_length=1, max_length=100, description="Javon joylashuvi (masalan: '2-qavat, A-3 javon')")
    status: str = Field(default="available", max_length=20, description="Kitob holati: available, borrowed, reserved")
    description: str | None = Field(default=None, description="Kitob haqida qisqacha tavsif")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255, description="Kitob nomi")
    author: str | None = Field(default=None, min_length=1, max_length=255, description="Kitob muallifi")
    genre: str | None = Field(default=None, min_length=1, max_length=100, description="Kitob janri")
    year: int | None = Field(default=None, ge=0, le=2100, description="Nashr etilgan yili")
    shelf_location: str | None = Field(default=None, min_length=1, max_length=100, description="Javon joylashuvi")
    status: str | None = Field(default=None, max_length=20, description="Kitob holati: available, borrowed, reserved")
    description: str | None = Field(default=None, description="Kitob haqida qisqacha tavsif")


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    items: list[BookResponse]
    total: int
    skip: int
    limit: int


class BookFilterParams(BaseModel):
    query: str | None = Field(default=None, description="Kitob nomi yoki muallif bo'yicha qidiruv")
    genre: str | None = Field(default=None, description="Janr bo'yicha filtr")
    author: str | None = Field(default=None, description="Muallif ismi bo'yicha filtr")
    status: str | None = Field(default=None, description="Kitob holati: available, borrowed, reserved")
    year_from: int | None = Field(default=None, ge=0, le=2100, description="Nashr yilining quyi chegarasi")
    year_to: int | None = Field(default=None, ge=0, le=2100, description="Nashr yilining yuqori chegarasi")
    sort_by: str = Field(default="id", description="Saralash maydoni: id, title, year, created_at")
    order: str = Field(default="desc", description="Saralash tartibi: asc yoki desc")
    skip: int = Field(default=0, ge=0, description="O'tkazib yuboriladigan yozuvlar soni")
    limit: int = Field(default=20, ge=1, le=100, description="Qaytariladigan maksimal yozuvlar soni")


class BookSearchResultResponse(BaseModel):
    items: list[BookResponse]
    total: int
    skip: int
    limit: int
    ask_ai: bool = Field(default=False, description="Kitob topilmaganda AI Agentiga yo'naltirish bayrog'i")
    suggestions: list[str] = Field(default_factory=list, description="Foydalanuvchiga tavsiyalar ro'yxati")
