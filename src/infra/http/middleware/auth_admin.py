from datetime import timedelta, datetime

import os

import jwt

from fastapi import HTTPException


class TokenHandler:
    """"""

    def create_token(id_admin: int):
        """create token"""
        try:
            key_app = os.getenv("SECRET_KEY")
            payload = {"id": id_admin, "exp": datetime.utcnow() + timedelta(days=1)}
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token
