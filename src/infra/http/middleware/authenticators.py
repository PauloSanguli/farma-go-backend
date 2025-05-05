import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from src.domain.enums import UserRole


class JwtHandler:
    """"""

    @classmethod
    def encode_token_for_entity(cls, entity_role: str, entity_id: str) -> str:
        try:
            key_app = os.getenv("SECRET-KEY")
            payload = {
                "role": entity_role,
                "id": entity_id,
                "exp": datetime.utcnow() + timedelta(days=1),
            }
            token = jwt.encode(payload, key_app)
        except jwt.PyJWKError:
            raise HTTPException(status_code=400, detail="error creating the token")
        return token

    @classmethod
    def create_token_admin(cls, admin_id: str) -> str | None:
        """create token for admin"""
        return cls.encode_token_for_entity(
            entity_role=UserRole.ADMIN, entity_id=admin_id
        )

    @classmethod
    def create_token_pharmacist(cls, pharmacist_id: str) -> str | None:
        """create token for pharmacist"""
        return cls.encode_token_for_entity(
            entity_role=UserRole.PHARMACIST, entity_id=pharmacist_id
        )

    @classmethod
    def create_token_user(cls, user_id: str) -> str | None:
        """create token for user"""
        return cls.encode_token_for_entity(entity_role=UserRole.USER, entity_id=user_id)
