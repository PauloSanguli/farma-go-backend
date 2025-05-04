import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from src.domain.enums import UserRole


class TokenHandler:
    """"""
    @classmethod
    def encode_token_for_entity(cls, entity_role: str, entity_id: str) -> str:
        try:
            key_app = os.getenv("SECRET_KEY")
            payload = {
                "role": entity_role,
                "id": entity_id,
                "exp": datetime.utcnow() + timedelta(days=1),
            }
            cls.token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")

    @classmethod
    def create_token_admin(cls, admin_id: str) -> str | None:
        """create token"""
        try:
            key_app = os.getenv("SECRET_KEY")
            payload = {
                "role": UserRole.ADMIN,
                "id": admin_id,
                "exp": datetime.utcnow() + timedelta(days=1),
            }
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token
    

    @classmethod
    def create_token_pharmacist(cls, pharmacist_id: str) -> str | None:
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

    @classmethod
    def create_token_user(cls, user_id: str) -> str | None:
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
