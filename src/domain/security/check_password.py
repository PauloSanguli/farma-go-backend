"""method for check password encrypted"""

import bcrypt
from fastapi import HTTPException


def check_password_hashed(pwd: str, pwd_hashed: str) -> bool:
    try:
        result = bcrypt.checkpw(pwd.encode("utf-8"), pwd_hashed.encode("utf-8"))
    except Exception as error:
        raise HTTPException(detail="invalid password encrypt format", status_code=400)
    return result
