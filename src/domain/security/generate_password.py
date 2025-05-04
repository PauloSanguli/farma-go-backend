"""method for encrypt password"""

import bcrypt


def has_password(pwd: str) -> any:
    salt = bcrypt.gensalt()
    pwd_hashed = bcrypt.hashpw(pwd.encode("utf-8"), salt)

    return pwd_hashed
