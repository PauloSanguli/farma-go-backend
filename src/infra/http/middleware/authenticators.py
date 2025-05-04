import os

import jwt

from datetime import datetime, timedelta

from fastapi import HTTPException

from src.domain.enums import UserRole



class TokenHandler:
    """"""
    def create_token_admin(admin_id: str) -> str | None:
        """create token"""
        try:
            key_app = os.getenv("SECRET_KEY")
            payload = {
                "role": UserRole.ADMIN,
                "id": admin_id,
                "exp": datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token


    def create_token_pharmacist(pharmacist_id: str) -> str | None:
        """create token"""
        try:
            key_app = os.getenv("SECRET-KEY")
            payload = {
                "role": UserRole.PHARMACIST,
                "id": pharmacist_id,
                "exp": datetime.utcnow() + timedelta(days=1),
            }
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token


    def create_token_user(user_id: str) -> str | None:
        """create token"""
        try:
            key_app = os.getenv("SECRET-KEY")
            payload = {
                "role": UserRole.USER,
                "id": user_id,
                "exp": datetime.utcnow() + timedelta(days=1),
            }
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token
