# [Fayl maqsadi: Foydalanuvchi ma'lumotlari uchun Pydantic DTO sxemalari]
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    email: str = Field(description="Foydalanuvchi elektron pochtasi")
    username: str = Field(min_length=3, max_length=100, description="Noyob foydalanuvchi nomi")
    full_name: str | None = Field(default=None, max_length=255, description="Foydalanuvchi to'liq ismi")
    role: str = Field(default="user", description="Foydalanuvchi roli (admin/user/librarian)")


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100, description="Foydalanuvchi maxfiy so'zi")


class UserUpdate(BaseModel):
    email: str | None = Field(default=None, description="Yangi elektron pochta")
    username: str | None = Field(default=None, min_length=3, max_length=100, description="Yangi foydalanuvchi nomi")
    full_name: str | None = Field(default=None, max_length=255, description="Yangi to'liq ism")
    password: str | None = Field(default=None, min_length=6, max_length=100, description="Yangi maxfiy so'z")
    role: str | None = Field(default=None, description="Yangi rol")
    is_active: bool | None = Field(default=None, description="Faollik holati")


class UserResponse(UserBase):
    id: int = Field(description="Foydalanuvchi unikal ID raqami")
    is_active: bool = Field(description="Akkaunt faollik holati")
    created_at: datetime = Field(description="Ro'yxatdan o'tgan vaqt")

    model_config = ConfigDict(from_attributes=True)
