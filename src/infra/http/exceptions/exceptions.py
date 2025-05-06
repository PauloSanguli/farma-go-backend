from fastapi import status
from fastapi.exceptions import HTTPException

class InvalidTokenProvidedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your signature was expired or invalid"
        )

class PermissionDeniedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
