import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from src.domain.enums import EntityRole
from src.infra.models import Pharmacist


class JwtHandler:
    """"""

    @classmethod
    def encode_token_for_entity(cls, payload: dict[str, str]) -> str:
        try:
            key_app = os.getenv("SECRET-KEY", "")
            payload["exp"] = datetime.utcnow() + timedelta(days=1)
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token

    @classmethod
    def create_token_admin(cls, admin_id: str) -> str | None:
        """create token for admin"""
        payload = payload = {
            "role": EntityRole.ADMIN,
            "id": admin_id,
        }
        return cls.encode_token_for_entity(payload)

    @classmethod
    def create_token_pharmacist(cls, pharmacist: Pharmacist) -> str | None:
        """create token for pharmacist"""
        payload = payload = {
            "id": pharmacist.id,
            "role": EntityRole.PHARMACIST,
            "tennant": pharmacist.pharmacy_id,
        }
        return cls.encode_token_for_entity(payload)

    @classmethod
    def create_token_user(cls, user_id: str) -> str | None:
        """create token for user"""
        payload = payload = {
            "role": EntityRole.USER,
            "id": user_id,
        }
        return cls.encode_token_for_entity(payload)
