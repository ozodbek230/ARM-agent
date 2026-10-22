# [Fayl maqsadi: Ijara va bron uchun Pydantic v2 sxemalari]
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.book import BookResponse
from backend.app.schemas.user import UserResponse


class BorrowCreate(BaseModel):
    book_id: int = Field(..., description="Ijaraga olinayotgan kitob identifikatori")
    days: int = Field(default=14, ge=1, le=30, description="Ijara muddati (kunlar soni, sukut bo'yicha 14 kun)")


class ReturnRequest(BaseModel):
    book_id: int | None = Field(default=None, description="Qaytarilayotgan kitob ID si")
    borrow_id: int | None = Field(default=None, description="Ijara yozuvi ID si")


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    returned_date: datetime | None = None
    status: str
    book: BookResponse | None = None
    user: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class BorrowListResponse(BaseModel):
    items: list[BorrowResponse]
    total: int


class ReservationCreate(BaseModel):
    book_id: int = Field(..., description="Bron qilinayotgan kitob identifikatori")


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    reserved_at: datetime
    queue_position: int
    status: str
    book: BookResponse | None = None
    user: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class ReservationListResponse(BaseModel):
    items: list[ReservationResponse]
    total: int
