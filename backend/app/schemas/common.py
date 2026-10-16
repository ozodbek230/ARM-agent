# [Fayl maqsadi: Umumiy Pydantic sxemalar (Pagination, Message, Error)]
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="O'tkazib yuboriladigan yozuvlar soni")
    limit: int = Field(default=20, ge=1, le=100, description="Qaytariladigan maksimal yozuvlar soni")


class MessageResponse(BaseModel):
    message: str = Field(description="Xabar matni")


class ErrorResponse(BaseModel):
    detail: str = Field(description="Xatolik tafsiloti")
