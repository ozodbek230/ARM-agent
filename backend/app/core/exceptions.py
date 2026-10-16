# [Fayl maqsadi: Tizim bo'yicha maxsus HTTP xatoliklar (Custom Exceptions)]
from typing import Any
from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resurs topilmadi", headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)


class UnauthorizedError(HTTPException):
    def __init__(
        self,
        detail: str = "Avtorizatsiyadan o'tilmagan yoki token yaroqsiz",
        headers: dict[str, Any] | None = None
    ) -> None:
        auth_headers = {"WWW-Authenticate": "Bearer"}
        if headers:
            auth_headers.update(headers)
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=auth_headers)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Ushbu amalni bajarish uchun huquq yetarli emas", headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)


class BadRequestError(HTTPException):
    def __init__(self, detail: str = "Noto'g'ri so'rov yuborildi", headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)


class ConflictError(HTTPException):
    def __init__(self, detail: str = "Ma'lumotlar to'qnashuvi yuz berdi", headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, headers=headers)
