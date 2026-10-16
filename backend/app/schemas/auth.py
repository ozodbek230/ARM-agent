# [Fayl maqsadi: Autentifikatsiya uchun Pydantic sxemalari (Login, Token, Refresh)]
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(description="Foydalanuvchi nomi yoki elektron pochtasi")
    password: str = Field(description="Foydalanuvchi paroli")


class TokenResponse(BaseModel):
    access_token: str = Field(description="JWT Access token")
    refresh_token: str = Field(description="JWT Refresh token")
    token_type: str = Field(default="bearer", description="Token turi")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(description="Yangi access token olish uchun refresh token")


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None
