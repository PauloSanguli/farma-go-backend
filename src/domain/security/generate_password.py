"""method for encrypt password"""

import bcrypt


def hash_password(pwd: str) -> str:
    salt = bcrypt.gensalt()
    pwd_hashed = bcrypt.hashpw(pwd.encode("utf-8"), salt).decode()
    return pwd_hashed
