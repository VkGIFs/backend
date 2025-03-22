from typing import Any, Mapping, Optional

from starlette import status


class ApiException(Exception):
    """
    Base class for API exceptions
    """

    def __init__(self, code: int, error: str) -> None:
        super().__init__()
        self.message = error
        self.status_code = code


class InternalServerError(Exception):
    """500 Internal Server Error"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Ахуеть! Ты всё сломал!"

    def __init__(self, message: Optional[str] = None, debug: Any = None) -> None:
        self.message = message or self.message
        self.debug = debug

    @classmethod
    def code(cls):
        """Really need descriptions?"""

        return cls.__name__

    def to_json(self) -> Mapping:
        """Ok. This is json return from InternalServerError class"""
        return {
            "code": self.status_code,
            "message": self.message,
            "debug": self.debug,
        }


class UserAlreadyRegisteredError(ApiException):
    """400 User already registered error"""

    def __init__(self) -> None:
        super().__init__(400, "Такой пользователь уже зарегистрирован!")
