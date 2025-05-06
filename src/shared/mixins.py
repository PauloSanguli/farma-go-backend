from fastapi import status
from fastapi.exceptions import HTTPException

from src.domain.security import check_password_hashed, hash_password


class PasswordMixin:
    password: str

    def _encrypt_password(self, password: str | None = None) -> None:
        self.password = hash_password(password or self.password)

    def _check_password(self, password: str | None) -> bool:
        if not check_password_hashed(password, self.password):
            raise HTTPException(
                detail="Invalid password provided",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return check_password_hashed(password, self.password)
